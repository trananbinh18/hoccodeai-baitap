import random
import string
import tkinter as tk
from tkinter import filedialog
from prompt_toolkit import prompt
from colorama import Fore, Back, Style, init

# Functions Begin
def clean_mesages():
    global messages
    messages = []

def open_file_picker():
    root = tk.Tk()
    root.withdraw()
    print("Notice: file picker window is openning. Please select a file.")
    file_path = filedialog.askopenfilename()
    return file_path

def print_debug_stack():
    global messages
    print("Messages Array:", messages)
    

def generate_random_string(length, characters=None):
    """
    Generates a random string of a specified length.

    Args:
        length (int): The desired length of the random string.
        characters (str, optional): A string containing the pool of characters
                                    to choose from. If None, it defaults to
                                    ascii letters and digits.

    Returns:
        str: The randomly generated string.
    """
    if characters is None:
        characters = string.ascii_letters + string.digits
    
    # Use random.choices for more efficient selection of multiple characters
    # and then join them into a single string.
    random_chars = random.choices(characters, k=length)
    return "".join(random_chars)


def continuous_chat():
    global messages
    while True:
        user_input = prompt("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting chat. Goodbye!")
            break
        elif user_input.lower() == "file":
            file_path = open_file_picker()
            if file_path:
                print(f"Selected file: '{file_path}' attached to the message.")
                continue
            else:
                print("No file selected.")
                continue
        elif user_input.lower() == "debug":
            print_debug_stack()
            continue
        
        messages.append({"role": "user", "content": user_input})
        assistant_response = f"{generate_random_string(20)}"
        messages.append({"role": "assistant", "content": assistant_response})
        
        print(f"{Fore.BLUE}Assistant: {assistant_response}")
# Functions end

# Initialization settings begin
init(autoreset=True)
# Initialization settings end
print(f"""
Hi tui là một một trợ lý ảo, tui có thể giúp gì cho bạn?
{Fore.YELLOW} 
Guides: 
- 🚪 gõ 'exit'|'quit'|'q' để thoát.
- 📙 gõ 'file' để mở cửa sổ chọn file.
- 🐞 gõ 'debug' in ra các biến.
""")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

continuous_chat()
    
