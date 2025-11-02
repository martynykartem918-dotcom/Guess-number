from customtkinter import *
import random

set_appearance_mode("dark")
set_default_color_theme("blue")

window = CTk()
window.title("Guess the Number")
window.geometry("800x500")
window.resizable(False, False)

difficulty = StringVar(value="")
target_number = None
points = 0
game_running = False
admin_mode_active = False
buttons = []

ADMIN_PASSWORD = "253876"

left_frame = CTkFrame(window)
left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

info_label = CTkLabel(left_frame, text="", font=("Arial", 14), wraplength=250, justify="left")
info_label.pack(fill="x", expand=True, pady=10)

def show_info(level):
    info = {
        "Normal": "Range 1–10\nGives 5 points",
        "Medium": "Range 1–25\nGives 10 points",
        "Hard": "Range 1–50\nGives 25 points",
        "Impossible": "Range 1–100\nGives ??? points",
    }
    def update_text():
        info_label.configure(text=info[level], wraplength=left_frame.winfo_width())
    left_frame.after(50, update_text)

def start_game():
    global target_number, game_running
    if not difficulty.get():
        status_label.configure(text="Select difficulty first!")
        return
    game_running = True
    entry.configure(state="normal")
    status_label.configure(text="Game started! Enter your guess.")
    entry.delete(0, END)
    new_secret()

def stop_game():
    global game_running
    game_running = False

def disable_all_controls():
    entry.configure(state="disabled")
    for btn in buttons:
        btn.configure(state="disabled")

def get_range():
    ranges = {"Normal":10, "Medium":25, "Hard":50, "Impossible":100}
    return ranges[difficulty.get()]

def get_points():
    pts = {"Normal":5, "Medium":10, "Hard":25, "Impossible":50}
    return pts[difficulty.get()]

def new_secret():
    global target_number
    if difficulty.get():
        target_number = random.randint(1, get_range())

def apply_guess():
    global target_number, points
    if not difficulty.get() or not game_running:
        status_label.configure(text="Start game first!")
        return
    if target_number is None:
        new_secret()
    try:
        guess = int(entry.get())
    except ValueError:
        status_label.configure(text="Enter a number!")
        return
    if guess == target_number:
        points += get_points()
        points_label.configure(text=f"Points: {points}")
        status_label.configure(text=f"Correct! It was {target_number}.")
        new_secret()
    else:
        status_label.configure(text=f"Wrong! Try again.")
    entry.delete(0, END)

def give_up():
    stop_game()
    disable_all_controls()
    status_label.configure(text=f"You gave up! You collected {points} points.")

def toggle_admin_mode():
    global admin_mode_active
    if admin_mode_active:
        admin_entry.pack_forget()
        admin_label.pack_forget()
        admin_mode_active = False
    else:
        admin_entry.pack(pady=5)
        admin_label.pack(pady=5)
        admin_mode_active = True

def check_admin_password(event=None):
    if admin_entry.get() == ADMIN_PASSWORD:
        if target_number is not None:
            admin_label.configure(text=f"Secret number: {target_number}", text_color="orange")
        else:
            admin_label.configure(text="No number yet!", text_color="gray")
    else:
        admin_label.configure(text="Wrong password!", text_color="red")

CTkLabel(left_frame, text="Select difficulty:", font=("Arial", 18)).pack(pady=(10,20))

def make_option(name):
    frame = CTkFrame(left_frame)
    frame.pack(fill="x", pady=8)
    radio = CTkRadioButton(frame, text=name, variable=difficulty, value=name)
    radio.pack(side="left", fill="x", expand=True, padx=(0,5))
    info_btn = CTkButton(frame, text="i", width=30, height=30, fg_color="#2a2a2a", corner_radius=15, command=lambda: show_info(name))
    info_btn.pack(side="right")
    buttons.append(radio)
    buttons.append(info_btn)

for name in ["Normal", "Medium", "Hard", "Impossible"]:
    make_option(name)

start_btn = CTkButton(left_frame, text="Start", command=start_game)
start_btn.pack(pady=30, side="bottom")
buttons.append(start_btn)

right_frame = CTkFrame(window)
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

CTkLabel(right_frame, text="Guess the Number Game", font=("Arial", 20, "bold")).pack(pady=10)

entry = CTkEntry(right_frame, placeholder_text="Enter your number", state="disabled")
entry.pack(pady=20, fill="x", padx=40)

apply_btn = CTkButton(right_frame, text="Apply", command=apply_guess, fg_color="green")
apply_btn.pack(pady=10)
buttons.append(apply_btn)

status_label = CTkLabel(right_frame, text="", font=("Arial", 16))
status_label.pack(pady=10)

points_label = CTkLabel(right_frame, text="Points: 0", font=("Arial", 14))
points_label.pack(pady=10)

give_up_btn = CTkButton(right_frame, text="Give Up", fg_color="red", command=give_up)
give_up_btn.pack(pady=10)
buttons.append(give_up_btn)

admin_btn = CTkButton(right_frame, text="Admin Mode", fg_color="#444", command=toggle_admin_mode)
admin_btn.pack(pady=10)
buttons.append(admin_btn)

admin_entry = CTkEntry(right_frame, placeholder_text="Enter 6-digit password", show="*")
admin_entry.bind("<Return>", check_admin_password)

admin_label = CTkLabel(right_frame, text="", font=("Arial", 14))

window.mainloop()
