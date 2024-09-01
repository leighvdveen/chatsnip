import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup

def extract_chat_from_html(html_file, chat_name):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    chat = soup.find('div', {'class': 'chat-name'}, string=chat_name)
    
    if chat:
        chat_content = chat.find_parent('div', {'class': 'chat-history'})
        if chat_content:
            return chat_content.get_text(separator='\n').strip()
    return None

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        entry_html_file.delete(0, tk.END)
        entry_html_file.insert(0, file_path)

def extract_chat():
    html_file = entry_html_file.get()
    chat_name = entry_chat_name.get()
    
    if not os.path.exists(html_file):
        messagebox.showerror("Error", "HTML file does not exist.")
        return
    
    chat_content = extract_chat_from_html(html_file, chat_name)
    
    if chat_content:
        output_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")])
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write(chat_content)
            messagebox.showinfo("Success", f"Chat content saved to {output_file}")
    else:
        messagebox.showerror("Error", "Chat not found or content could not be extracted.")

# GUI setup
root = tk.Tk()
root.title("Chat Extractor")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_html_file = tk.Label(frame, text="HTML File:")
label_html_file.grid(row=0, column=0, sticky="e")
entry_html_file = tk.Entry(frame, width=50)
entry_html_file.grid(row=0, column=1, padx=5)
button_browse = tk.Button(frame, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2)

label_chat_name = tk.Label(frame, text="Chat Name:")
label_chat_name.grid(row=1, column=0, sticky="e")
entry_chat_name = tk.Entry(frame, width=50)
entry_chat_name.grid(row=1, column=1, padx=5)

button_extract = tk.Button(frame, text="Extract Chat", command=extract_chat)
button_extract.grid(row=2, columnspan=3, pady=10)

root.mainloop()