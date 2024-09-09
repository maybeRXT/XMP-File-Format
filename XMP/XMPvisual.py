import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import subprocess
import re
import XMPmain  # Assuming XMPmain.py is in the same directory

class XMPEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("XMP Editor")
        self.filepath = None

        # Create text editor with dark mode
        self.text_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, undo=True, bg='#2e2e2e', fg='#ffffff', insertbackground='white')
        self.text_editor.pack(fill=tk.BOTH, expand=1)

        # Create menu
        self.create_menu()

        # Bind shortcuts
        self.bind_shortcuts()

        # Syntax highlighting
        self.text_editor.bind("<KeyRelease>", self.syntax_highlighting)
        self.text_editor.bind("<Return>", self.auto_indent)

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Export as EXE", command=self.export_as_exe)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        run_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run", command=self.run_file, accelerator="Ctrl+R")
        run_menu.add_command(label="Debug", command=self.debug_file, accelerator="Ctrl+D")

    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-r>", lambda event: self.run_file())
        self.root.bind("<Control-d>", lambda event: self.debug_file())

    def new_file(self):
        self.filepath = None
        self.text_editor.delete(1.0, tk.END)

    def open_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("XMP files", "*.xmp")])
        if self.filepath:
            with open(self.filepath, 'r') as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)
                self.syntax_highlighting()

    def save_file(self):
        if self.filepath:
            with open(self.filepath, 'w') as file:
                content = self.text_editor.get(1.0, tk.END)
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        self.filepath = filedialog.asksaveasfilename(defaultextension=".xmp", filetypes=[("XMP files", "*.xmp")])
        if self.filepath:
            with open(self.filepath, 'w') as file:
                content = self.text_editor.get(1.0, tk.END)
                file.write(content)

    def run_file(self):
        if self.filepath:
            XMPmain.XMPFile(self.filepath)  # Assuming XMPmain.py has a class XMPFile

    def debug_file(self):
        if self.filepath:
            # Placeholder for debug functionality
            messagebox.showinfo("Debug", "Debugging not implemented yet.")

    def export_as_exe(self):
        if self.filepath:
            exe_path = filedialog.asksaveasfilename(defaultextension=".exe", filetypes=[("Executable files", "*.exe")])
            if exe_path:
                subprocess.call(['pyinstaller', '--onefile', '--name', os.path.basename(exe_path), self.filepath])
                messagebox.showinfo("Export as EXE", "Exported successfully!")

    def syntax_highlighting(self, event=None):
        self.text_editor.tag_remove("orange", "1.0", tk.END)
        self.text_editor.tag_remove("green", "1.0", tk.END)
        self.text_editor.tag_remove("purple", "1.0", tk.END)
        self.text_editor.tag_remove("blue", "1.0", tk.END)
        self.text_editor.tag_remove("yellow", "1.0", tk.END)
        self.text_editor.tag_remove("red", "1.0", tk.END)

        patterns = {
            "orange": r"\$xmp\b",
            "green": r"\b\w+\b",
            "purple": r"\b(if|else|for|while|def)\b|[+\-*/=<>]",
            "blue": r"\bdef\b",
            "yellow": r"[()]",
            "red": r"\bcontainer\b"
        }

        for tag, pattern in patterns.items():
            start = "1.0"
            while True:
                start = self.text_editor.search(pattern, start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(self.text_editor.get(start, start + ' wordend'))}c"
                self.text_editor.tag_add(tag, start, end)
                start = end

        self.text_editor.tag_config("orange", foreground="orange")
        self.text_editor.tag_config("green", foreground="green")
        self.text_editor.tag_config("purple", foreground="purple")
        self.text_editor.tag_config("blue", foreground="blue")
        self.text_editor.tag_config("yellow", foreground="yellow")
        self.text_editor.tag_config("red", foreground="red")

    def auto_indent(self, event=None):
        current_line = self.text_editor.get("insert linestart", "insert lineend")
        if current_line.strip().endswith(":"):
            self.text_editor.insert("insert", "\n" + " " * 4)
            return "break"

def main():
    root = tk.Tk()
    editor = XMPEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
