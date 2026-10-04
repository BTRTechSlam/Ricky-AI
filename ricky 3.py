from tkinter import *
import os
from datetime import datetime

from PIL.ImageStat import Global
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from PIL.ImageOps import expand

model = OllamaModel(
    "qwen3:0.6b",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

NOTES_FILE = "notes.txt"

def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

def calculate(expression: str) -> str:
    """Evaluate a basic math expression, e.g. '23 * 7 + 1'."""
    if not set(expression) <= set("0123456789+-*/(). "):
        return "Error: only numbers and + - * / ( ) are allowed."
    try:
        return str(eval(expression))
    except Exception as error:
        return f"Error: {error}"

def save_note(note: str) -> str:
    """Save a short note so it can be recalled later."""
    with open(NOTES_FILE, "a", encoding="utf-8") as file:
        file.write(f"- {note}\n")
    return "Note saved."

def read_notes() -> str:
    """Read back all previously saved notes."""
    if not os.path.exists(NOTES_FILE):
        return "No notes saved yet."
    with open(NOTES_FILE, encoding="utf-8") as file:
        return file.read()

agent = Agent(
    model,
    tools=[get_current_time, calculate, save_note, read_notes],
    instructions="""You are Ricky Renaud, a cool, intelligent, and helpful personal AI assistant.

    Be confident, friendly, relaxed, and naturally conversational.
    Talk like a smart friend, not like a boring robot.
    Use simple language, light humor, and occasional emojis when appropriate.

    Give clear and useful answers.
    When something is complicated, break it down into simple steps.
    When teaching programming, explain what the code does and why it works.

    When helping me make decisions:
    - Show me the important options.
    - Explain the advantages and disadvantages.
    - Explain possible risks and consequences.
    - Help me think logically.
    - Don't pressure me into a decision.

    Be honest when you don't know something.
    Don't make information up.

    Your name is Ricky Renaud.
    You are my personal AI assistant for learning, creating, solving problems, and making informed decisions.

    Be useful, be creative, and keep the conversation natural.
    """,
)

history = []


def submit():
    global history

    user_input = textbar.get("1.0", "end-1c").strip()
    if not user_input:
        return

    result = agent.run_sync(user_input, message_history=history)
    history = result.all_messages()

    label.config(state=NORMAL)
    label.insert(END, "You: " + user_input + "\n")
    label.insert(END, "Ricky: " + result.output + "\n\n")
    label.config(state=DISABLED)
    label.see(END)

    textbar.delete("1.0", END)







def clear():
    pass


window = Tk()
window.geometry("500x500")

frame1 = Frame(window, bg="#c7c7c7")
frame1.pack()

frame2 = Frame(window)
frame2.pack()

#output bar ...................................................................
label = Text(frame1, bg="#c7c7c7", width=60,height=20, state=DISABLED)
scrollbar = Scrollbar(frame1, command=label.yview)
label.config(yscrollcommand=scrollbar.set)
label.grid(row=0, column=0, )
scrollbar.grid(row=0, column=1,rowspan=1 , sticky='ns')



#input bar...........................................................
#input = Entry(frame2, bg="#f0efbf" , width=65 )
#input.pack()
textbar = Text(frame2, width=40, height=7 , bg="#f0efbf", wrap=WORD)
scrollbar1 = Scrollbar(frame2, command=textbar.yview)
textbar.config(yscrollcommand=scrollbar1.set)
scrollbar1.grid(column=1 , row=0 , sticky="ns" , rowspan=2)
textbar.grid(row=0, column=0, rowspan=2)


button1 = Button(frame2 ,text="submit", width=5 , height=2 , command=submit)
button1.grid(row=0, column=2)
button2 = Button(frame2 ,text="clear", width=5 , height=2)
button2.grid(row=1, column=2)








window.mainloop()