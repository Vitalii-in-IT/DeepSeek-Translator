import keyboard
import pyperclip
import requests
import time
import threading
import tkinter as tk
from tkinter import ttk
import json
import os

last_output = None
CONFIG_FILE = "config.json"

# ================= CONFIG =================

config = {
    "api_key": "",
    "target_lang": "English",
    "bring_to_front": False
}

def bring_window_front():
    try:
        root.deiconify()      # if it was folded
        root.lift()           # raise the window
        root.focus_force()    # give focus
    except:
        pass

def load_config():
    global config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# ================= DEEPSEEK =================

def translate_text(text):
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }

    prompt = f"Translate the following text to {config['target_lang']}:\n\n{text}"

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("API ERROR:", e)
        return "[ERROR]"

# ================= MAIN ACTION =================

def process_text():
    global last_output

    try:
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.3)

        text = pyperclip.paste()

        if not text.strip():
            return

        translated = translate_text(text)

        # Saving for GUI
        last_output = translated

        # Updating the GUI (if the window is open)
        try:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, translated)
        except:
            pass

        # insert back
        pyperclip.copy(translated)
        time.sleep(0.1)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)


        # Raise the window if it is on
        if config.get("bring_to_front"):
            try:
                root.after(0, bring_window_front)
            except:
                pass

    except Exception as e:
        print("PROCESS ERROR:", e)

# ================= HOTKEY =================
def paste_api():
    try:
        text = pyperclip.paste().strip()
        if text:
            api_entry.delete(0, tk.END)
            api_entry.insert(0, text)
            config["api_key"] = text
            save_config()
            status_label.config(text="API pasted ✅")
    except Exception as e:
        status_label.config(text="Paste error ❌")
        print("PASTE ERROR:", e)

def hotkey_listener():
    keyboard.add_hotkey("ctrl+space", process_text)
    keyboard.wait()

# ================= GUI =================

def save_api():
    config["api_key"] = api_entry.get()
    save_config()
    status_label.config(text="API saved ✅")

def change_language(event):
    config["target_lang"] = lang_combo.get()
    save_config()

def start_gui():
    global root
    root = tk.Tk()
    root.title("DeepSeek Translator")
    root.geometry("300x300")

    tk.Label(root, text="API Key").pack(pady=5)

    global api_entry
    api_entry = tk.Entry(root, width=35)
    api_entry.insert(0, config["api_key"])
    api_entry.pack()

    frame = tk.Frame(root)
    frame.pack(pady=5)

    tk.Button(frame, text="Save API", command=save_api).pack(side="left", padx=5)
    tk.Button(frame, text="Paste API", command=paste_api).pack(side="left", padx=5)

    tk.Label(root, text="Target Language").pack(pady=5)

    bring_var = tk.BooleanVar(value=config.get("bring_to_front", False))

    def toggle_bring():
        config["bring_to_front"] = bring_var.get()
        save_config()

    tk.Checkbutton(
        root,
        text="Bring to front after translate",
        variable=bring_var,
        command=toggle_bring
    ).pack(pady=5)

    global lang_combo
    lang_combo = ttk.Combobox(
        root,
        values=[
            "English",
            "Polish",
            "German",
            "Ukrainian",
            "Russian",
            "Spanish",
            "French"
        ],
        state="readonly"
    )

    lang_combo.set(config["target_lang"])
    lang_combo.pack()

    lang_combo.bind("<<ComboboxSelected>>", change_language)

    global status_label
    status_label = tk.Label(root, text="")
    status_label.pack(pady=3)

    tk.Label(root, text="Last Result").pack(pady=3)

    global result_text
    result_text = tk.Text(root, height=5, width=35)
    result_text.pack(pady=5)

    root.mainloop()

# ================= RUN =================

load_config()

threading.Thread(target=hotkey_listener, daemon=True).start()

start_gui()
