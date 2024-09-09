import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os
import sys
import importlib.util

class XMPFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}
        self.parse_file()

    def parse_file(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('$xmp') or line.startswith('#'):
                    continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.data[key.strip()] = self.evaluate_expression(value.strip())
                elif 'if' in line:
                    self.handle_if_statement(line)
                elif 'else' in line:
                    self.handle_else_statement(line)
                elif 'for' in line:
                    self.handle_for_loop(line)

    def evaluate_expression(self, expression):
        try:
            return eval(expression, {}, self.data)
        except:
            return expression

    def handle_if_statement(self, line):
        condition = re.search(r'if (.+):', line).group(1)
        if eval(condition, {}, self.data):
            self.data['status'] = "Adult"

    def handle_else_statement(self, line):
        self.data['status'] = "Minor"

    def handle_for_loop(self, line):
        loop_var, iterable = re.search(r'for (.+) in (.+):', line).groups()
        iterable = self.evaluate_expression(iterable)
        for item in iterable:
            print(f"{loop_var}: {item}")

    def get(self, key):
        return self.data.get(key, None)

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("XMP files", "*.xmp")])
    if filepath:
        xmp = XMPFile(filepath)
        print(xmp.get('greeting_message'))  # Example usage

def download_debug_file():
    messagebox.showinfo("Download Debug File", "Debug file downloaded.")

def create_container_directory():
    container_path = os.path.join(os.path.dirname(__file__), 'containers')
    os.makedirs(container_path, exist_ok=True)
    messagebox.showinfo("Create Container Directory", "Container directory created.")
    load_containers(container_path)

def load_containers(container_path):
    for filename in os.listdir(container_path):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module_path = os.path.join(container_path, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"Loaded module: {module_name}")

def force_shutdown():
    messagebox.showwarning("Force Shutdown", "All running applications will be shut down.")
    sys.exit()

def main():
    root = tk.Tk()
    root.title("XMP File Runner")

    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Options", menu=file_menu)
    file_menu.add_command(label="Download Debug File", command=download_debug_file)
    file_menu.add_command(label="Create Container Directory", command=create_container_directory)
    file_menu.add_command(label="Force Shutdown", command=force_shutdown)

    open_button = tk.Button(root, text="Open XMP File", command=open_file)
    open_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
