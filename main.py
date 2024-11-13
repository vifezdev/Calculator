import tkinter as tk
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()
root.title("Ultimate Calculator")
root.geometry("400x700")
root.resizable(False, False)

display_text = tk.StringVar(value="0")
expression = ""
current_theme = "dark"
history = []
memory = 0

themes = {
    "dark": {
        "bg": "#0E0E0E",
        "fg": "#66CCFF",
        "button_bg": "#1A1A1A",
        "button_fg": "#FFFFFF",
        "highlight": "#00CC99",
        "display_bg": "#1A1A1A",
        "display_fg": "#FFFFFF",
        "hover_bg": "#33334d"
    },
    "light": {
        "bg": "#F0F0F3",
        "fg": "#000000",
        "button_bg": "#D4D4D4",
        "button_fg": "#333333",
        "highlight": "#4CAF50",
        "display_bg": "#FFFFFF",
        "display_fg": "#000000",
        "hover_bg": "#E0E0E0"
    }
}

def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[theme_name]
    root.configure(bg=theme["bg"])
    display.configure(bg=theme["display_bg"], fg=theme["display_fg"])
    for btn in buttons:
        btn["bg"] = theme["button_bg"]
        btn["fg"] = theme["button_fg"]
        btn["activebackground"] = theme["highlight"]
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=theme["hover_bg"]))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=theme["button_bg"]))

def button_click(value):
    global expression
    global memory
    if value == "=":
        try:
            result = str(eval(expression))
            history.append(expression + " = " + result)
            display_text.set(result)
            expression = result
        except Exception:
            display_text.set("Error")
            expression = ""
    elif value == "C":
        expression = ""
        display_text.set("0")
    elif value == "H":
        show_history()
    elif value == "M+":
        memory += float(display_text.get())
        messagebox.showinfo("Memory Updated", f"Added {display_text.get()} to Memory.")
    elif value == "M-":
        memory -= float(display_text.get())
        messagebox.showinfo("Memory Updated", f"Subtracted {display_text.get()} from Memory.")
    elif value == "MR":
        display_text.set(str(memory))
        expression = str(memory)
    elif value == "MC":
        memory = 0
        messagebox.showinfo("Memory Cleared", "Memory has been cleared.")
    elif value == "Time":
        display_text.set(datetime.now().strftime("%H:%M:%S"))
    elif value == "Date":
        display_text.set(datetime.now().strftime("%Y-%m-%d"))
    elif value == "√":
        try:
            result = str(eval(expression) ** 0.5)
            display_text.set(result)
            expression = result
        except Exception:
            display_text.set("Error")
            expression = ""
    elif value == "±":
        if expression.startswith('-'):
            expression = expression[1:]
        else:
            expression = '-' + expression
        display_text.set(expression)
    else:
        if display_text.get() == "0":
            display_text.set("")
        expression += str(value)
        display_text.set(expression)

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("300x400")
    history_window.configure(bg=themes[current_theme]["bg"])

    history_label = tk.Label(history_window, text="History", font=("Helvetica", 16), bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
    history_label.pack(pady=10)

    for expr in history:
        label = tk.Label(history_window, text=expr, font=("Helvetica", 12), bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
        label.pack(anchor="w", padx=10)

def key_press(event):
    key = event.char
    if key.isdigit() or key in "+-*/.%()":
        button_click(key)
    elif key == "\r":
        button_click("=")
    elif key.lower() == "c":
        button_click("C")
    elif key == "h":
        button_click("H")
    elif key == ".":
        button_click(".")

root.bind("<Key>", key_press)

display = tk.Label(
    root, 
    textvariable=display_text, 
    font=("Helvetica", 48, "bold"), 
    anchor="e", 
    padx=10, 
    bg=themes[current_theme]["display_bg"], 
    fg=themes[current_theme]["display_fg"],
    relief="flat", 
    borderwidth=2
)
display.pack(fill="both", pady=(20, 10), padx=20)

button_frame = tk.Frame(root, bg=themes[current_theme]["bg"])
button_frame.pack(fill="both", expand=True, padx=20, pady=10)

button_texts = [
    ["C", "(", ")", "%"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
    ["√", "±", "Date", "Time"],
    ["M+", "M-", "MR", "MC"],
    ["H"]
]

buttons = []

for row_idx, row in enumerate(button_texts):
    for col_idx, text in enumerate(row):
        color = themes[current_theme]["highlight"] if text == "=" else themes[current_theme]["button_bg"]
        btn = tk.Button(
            button_frame,
            text=text,
            font=("Helvetica", 18, "bold"),
            fg=themes[current_theme]["button_fg"],
            bg=color,
            activebackground=themes[current_theme]["highlight"],
            activeforeground="white",
            command=lambda t=text: button_click(t),
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
        )
        btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=themes[current_theme]["hover_bg"]))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=themes[current_theme]["button_bg"]))
        buttons.append(btn)

for i in range(len(button_texts)):
    button_frame.rowconfigure(i, weight=1)
for i in range(4):
    button_frame.columnconfigure(i, weight=1)

def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("300x250")
    settings_win.configure(bg=themes[current_theme]["bg"])

    def switch_theme():
        new_theme = "light" if current_theme == "dark" else "dark"
        apply_theme(new_theme)

    theme_button = tk.Button(
        settings_win,
        text="Switch Theme",
        font=("Helvetica", 14, "bold"),
        command=switch_theme,
        bg=themes[current_theme]["button_bg"],
        fg=themes[current_theme]["fg"],
        activebackground=themes[current_theme]["highlight"],
        padx=20,
        pady=10,
    )
    theme_button.pack(pady=10)

    def clear_history():
        global history
        history = []
        messagebox.showinfo("History Cleared", "Calculation history has been cleared.")

    clear_history_button = tk.Button(
        settings_win,
        text="Clear History",
        font=("Helvetica", 14, "bold"),
        command=clear_history,
        bg=themes[current_theme]["button_bg"],
        fg=themes[current_theme]["fg"],
        activebackground=themes[current_theme]["highlight"],
        padx=20,
        pady=10,
    )
    clear_history_button.pack(pady=10)

menu_bar = tk.Menu(root)
settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Settings", command=open_settings)
menu_bar.add_cascade(label="Options", menu=settings_menu)
root.config(menu=menu_bar)

apply_theme(current_theme)

root.mainloop()