import tkinter as tk
from tkinter import filedialog
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from colorama import Fore, init, Back
from together import Together
import pymupdf
from docx import Document
import os
from transformers import AutoTokenizer
import shutil
import re
from pathlib import Path
from datetime import datetime




# Functions Begin
def get_screen_separator(char="=", color=Fore.GREEN):
    width = shutil.get_terminal_size().columns
    result = char * width
    return color+result

def open_file_picker():
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    root.focus_force()
    print(f"{Fore.YELLOW}Notice: file picker window is openning. Please select a file.")
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"), ("Word files", "*.docx")])
    root.destroy()
    return file_path

def open_file_saver(content, extension=".txt"):
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    root.focus_force()
    print()
    
    file_path = filedialog.asksaveasfilename(
        title="Save File",
        defaultextension=extension,
        initialdir=os.getcwd(),
        initialfile=f"final_{datetime.now().strftime("%Y%m%d%H%M%S")}{extension}",
        filetypes=[("Text files", f"*{extension}"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            Path(file_path).write_text(content, encoding='utf-8')
            print(f"{Fore.YELLOW}File saved successfully: {file_path}")
            return
        except Exception as e:
            print(f"{Fore.YELLOW}Error saving file: {e}")
            return
        
    print(f"{Fore.YELLOW}Save cancelled")
    root.destroy()
    return

def save_latest_file_content():
    global messages
    full_response = messages[len(messages) - 1]["content"]
    file_content = extract_tag_content(full_response, "screen-two")
    file_extension = extract_tag_content(full_response, "file-extension")
    if(file_content == "" or len(messages) == 1):
        print(f"{Fore.YELLOW}No file found in current response.")
        return
    open_file_saver(file_content, file_extension)
    

def extract_tag_content(text, tag_name):
    pattern = f'<{tag_name}>(.*?)</{tag_name}>'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return ""

def extract_pdf_content(file_path):
    result = ""
    doc = pymupdf.open(file_path)
    for page in doc:
        content = page.get_text()
        result += f"<page-{page.number}>{content}</page-{page.number}>"
        result += "\n"
    return f"<file-content>\n{result}\n</file-content>"

def extract_txt_content(file_path):
    result = ""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        result += f"<file-content>\n{content}\n</file-content>"
    return result

def extract_docx_content(file_path):
    result = ""
    doc = Document(file_path)
    for para in doc.paragraphs:
        result += f"<paragraph>{para.text}</paragraph>\n"
    return f"<file-content>\n{result}\n</file-content>"

def get_message_token(input_message):
    global messages, tokenizer
    flattened_input = f"{input_message['role']}:{input_message['content']}\n"
    tokens = tokenizer.encode(flattened_input)
    return len(tokens)

def print_debug_stack():
    global messages
    print("messages =", messages)
    print("current_token =", current_token)
    print("maximum_token =", maximum_token)
    print("debug_chunk_arr =", debug_chunk_arr)
    

def chat_response(user_input):
    global messages, client, debug_chunk_arr
    debug_chunk_arr = []
    messages = messages + [{"role": "user", "content": user_input}] 
    stream_response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages,
        stream=True,
        max_token=20
    )
    
    print(f"{Back.BLUE}🤖 Assistant: ", flush=True)
    messages = messages + [{"role": "assistant", "content": ""}]

    tag_buffer = ""
    is_having_file_extension = False

    for chunk in stream_response:
        chunk_content = chunk.choices[0].delta.content or ""
        messages[len(messages) - 1]["content"] += chunk_content
        
        # Handle tag detection
        if "<" in chunk_content:
            tag_buffer += chunk_content
            continue
        elif ">" in chunk_content:
            tag_buffer += chunk_content
            debug_chunk_arr.append(tag_buffer)
            
            # Process special tags
            if "<file-extension>" in tag_buffer:
                is_having_file_extension = True
            elif "<screen-two>" in tag_buffer:
                print(get_screen_separator())
            
            # Remove all special tags from buffer
            for tag in ["<screen-one>", "</screen-one>", "<screen-two>", "</screen-two>", "<screen-one>\n", "</screen-one>\n", "<screen-two>\n", "</screen-two>\n"]:
                tag_buffer = tag_buffer.replace(tag, "")
            
            # Extract clean content and remaining tag buffer
            if "<" in tag_buffer:
                clean_content = tag_buffer.split("<")[0]
                remaining_tag = tag_buffer.split("<", 1)[1]
                tag_buffer = f"<{remaining_tag}" if remaining_tag.strip() else ""
            else:
                clean_content = tag_buffer
                tag_buffer = ""
            
            # Print clean content if not finished rendering
            if clean_content and not is_having_file_extension and clean_content.strip() != "":
                print(Fore.BLUE + clean_content, end="", flush=True)
            
            continue
        else:
            # Handle regular content
            if tag_buffer:
                tag_buffer += chunk_content
            elif not is_having_file_extension:
                print(Fore.BLUE + chunk_content, end="", flush=True)

    if(is_having_file_extension):
        save_latest_file_content()

def continuous_chat():
    global messages, current_token
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
                    file_ext = os.path.splitext(file_path)[1].lower()
                    if file_ext == '.pdf':
                        user_input += extract_pdf_content(file_path)
                    if file_ext == '.txt' or file_ext == '.md':
                        user_input += extract_txt_content(file_path)
                    if file_ext == '.docx':
                        user_input += extract_docx_content(file_path)
                    print(f"Selected file: '{file_path}' and attached to your message.")
                    messages.append({"role": "user", "content": "Attached file: \n"+ user_input})
                else:
                    print("No file selected.")
                continue
            case "save":
                save_latest_file_content()
                continue
            case "debug":
                print_debug_stack()
                continue
            case "":
                continue

        chat_response(user_input)
        current_token += get_message_token(messages[len(messages) - 1])
        if current_token >= maximum_token:
            poped_message = messages.pop(1)
            current_token -= get_message_token(poped_message)
            continue
        print()


# Functions end

# Initialization settings begin
init(autoreset=True)
prompt_history = FileHistory('.my_cli_history')
system_prompt = """
You are a Multifunctional AI Assistant specialized in:
1. Content Translation with Humor
- When given a file content, translate it into the target language specified by the user.
- The translation must preserve the meaning, but you are allowed to add light humor, witty phrasing where appropriate.
- Output is your translate note (SCREEN ONE) and a single file containing the translated content (SCREEN TWO).
2. Summarization of Articles or Web Pages
- When given a URL or article content, summarize the key points with a maximum of 250 words.
- The summary must be clear and concise, but allow a humorous tone—sarcastic comments, light jokes, or witty remarks are allowed as long as the main information is intact.
- Do not use file output for this task.
3. Programming Exercise Solver
- When given a programming exercise (in Python or JavaScript), solve it correctly and return the solution as a code file.
- The solution must be direct, efficient, and correct.
- Include comments in the code explaining your approach.
- Do not return explanations outside the file. Only return the code file content.
- Output is solution Analysis (SCREEN-ONE) and a single file contain the solution's code (SCREEN-TWO).
4. General Conversation
- Engage in general conversation, answer questions, and provide information on various topics.
- The file output is not required for this tasks, but if really necessary, you can output a file content in (SCREEN-TWO).
General rules:
- Only 1 file output is allowed per response.
- Do not wrap the output in a code block.
- Only print tags screen-one and file-extension when they contain content
- Only output screen-one and file-extension when the output includes a file.
- Do not print any meta-notes or system explanations about whether a file was generated or not.
- Use emojis to make the conversation more engaging and fun.
- The output must be in the following format:
<screen-one>
[your response should be here (Required)]
</screen-one>
<screen-two>
[file content should be here (Optional)]
</screen-two>
<file-extension>
[the file extension is required if you output a file, e.g., .txt, .docx, .py, .js, .md]
</file-extension>
"""
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3")
client = Together()
messages = [
    {"role": "system", "content": system_prompt},
]
maximum_token = 28000
current_token = get_message_token(messages[0])

debug_chunk_arr = [

]
# Initialization settings end
print(f"""
{Fore.YELLOW} 
Guides: 
- 🚪 type 'exit'|'quit'|'q' to exit.
- 📙 type 'file' to open file picker.
- 💾 type 'save' to save the latest file content.
- 🐞 type 'debug' to print global val.
{Fore.BLUE}Hi there! I'm your AI Assistant. Let's chat!
""")
continuous_chat()
