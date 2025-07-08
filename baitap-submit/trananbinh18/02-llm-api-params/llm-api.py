import random
import string
import tkinter as tk
from tkinter import filedialog
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from colorama import Fore, init, Back, Style
from together import Together

# Functions Begin
def clean_mesages():
    global messages
    messages = []

def open_file_picker():
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    root.focus_force()
    print(f"{Fore.YELLOW}Notice: file picker window is openning. Please select a file.")
    file_path = filedialog.askopenfilename()
    return file_path

def print_debug_stack():
    global messages
    print("messages =", messages)
    

def chat_response(user_input):
    global messages, client
    messages = messages + [{"role": "user", "content": user_input}] 
    stream_response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages,
        stream=True,
        max_token=20
    )
    
    print(f"{Back.BLUE}🤖 Assistant: ", flush=True)
    messages = messages + [{"role": "assistant", "content": ""}]

    for chunk in stream_response:
        print(Fore.BLUE+chunk.choices[0].delta.content or "", end="", flush=True)
        messages[len(messages) - 1]["content"] += chunk.choices[0].delta.content or ""

    


def continuous_chat():
    global messages
    while True:
        print(f"{Back.CYAN}🥸  You: ")
        user_input = prompt("> ", history=prompt_history)
        match user_input:
            case "exit", "quit", "q":
                print("Exiting chat. Goodbye!")
                break
            case "file":
                file_path = open_file_picker()
                if file_path:
                    print(f"Selected file: '{file_path}' attached to the message.")
                else:
                    print("No file selected.")
                continue
            case "debug":
                print_debug_stack()
                continue
            case "":
                continue

        chat_response(user_input)
        print("\n")


# Functions end

# Initialization settings begin
init(autoreset=True)
prompt_history = FileHistory('.my_cli_history')
# Initialization settings end
print(f"""
{Fore.BLUE}Hi tui là một một trợ lý ảo, tui có thể giúp gì cho bạn?
{Fore.YELLOW} 
Guides: 
- 🚪 gõ 'exit'|'quit'|'q' để thoát.
- 📙 gõ 'file' để mở cửa sổ chọn file.
- 🐞 gõ 'debug' in ra các biến.
{Fore.BLUE}Chat:
""")

system_prompt = """
You are a helpful assistant.
"""

messages = [
    {"role": "system", "content": system_prompt},
]

client = Together(
)
continuous_chat()
    
