from customtkinter import *
import random

set_appearance_mode("dark")

window = CTk()
window.title("Guess the Number")
window.geometry("800x500")
window.resizable(False, False)

difficulty = StringVar(value="")
target_number = None
points = 0
game_running = False
admin_mode_active = False

ADMIN_PASSWORD = "135790"

def show_info(level):
    info = {
        "Normal": "Range 1–10\n5 points",
        "Medium": "Range 1–25\n10 points",
        "Hard": "Range 1–50\n25 points",
        "Impossible": "Range 1–100\n50 points",
    }
    info_label.configure(text=info[level])

def start_game():
    global target_number, game_running
    if not difficulty.get():
        status_label.configure(text="Select difficulty!")
        return
    game_running = True
    entry.configure(state="normal")
    target_number = random.randint(1, get_range())
    status_label.configure(text="Game started! Enter your guess.")

def get_range():
    return {"Normal":10, "Medium":25, "Hard":50, "Impossible":100}[difficulty.get()]

def get_points():
    return {"Normal":5, "Medium":10, "Hard":25, "Impossible":50}[difficulty.get()]

def apply_guess():
    global target_number, points
    if not game_running:
        status_label.configure(text="Press Start!")
        return
    try:
        guess = int(entry.get())
    except:
        status_label.configure(text="Enter number!")
        return
    if guess == target_number:
        points += get_points()
        points_label.configure(text=f"Points: {points}")
        status_label.configure(text="Correct!")
        target_number = random.randint(1, get_range())
    else:
        status_label.configure(text="Wrong!")
    entry.delete(0, END)

def give_up():
    global game_running
    game_running = False
    entry.configure(state="disabled")
    status_label.configure(text=f"You gave up. Total points: {points}")

def toggle_admin():
    global admin_mode_active
    if admin_mode_active:
        admin_entry.pack_forget()
        admin_label.pack_forget()
        admin_mode_active = False
    else:
        admin_entry.pack(pady=5)
        admin_label.pack(pady=5)
        admin_mode_active = True

def check_admin(event=None):
    if admin_entry.get() == ADMIN_PASSWORD:
        if target_number:
            admin_label.configure(text=f"Secret number: {target_number}", text_color="orange")
        else:
            admin_label.configure(text="No number yet!", text_color="gray")
    else:
        admin_label.configure(text="Wrong password!", text_color="red")

left = CTkFrame(window)
left.pack(side="left", fill="both", expand=True, padx=20, pady=20)

CTkLabel(left, text="Select difficulty:", font=("Arial", 18)).pack(pady=(10,20))
info_label = CTkLabel(left, text="", font=("Arial", 14))
info_label.pack(pady=10)

for name in ["Normal", "Medium", "Hard", "Impossible"]:
    f = CTkFrame(left)
    f.pack(fill="x", pady=5)
    CTkRadioButton(f, text=name, variable=difficulty, value=name).pack(side="left", padx=5)
    CTkButton(f, text="i", width=30, height=30, fg_color="#333", command=lambda n=name: show_info(n)).pack(side="right")

CTkButton(left, text="Start", command=start_game).pack(pady=30, side="bottom")

right = CTkFrame(window)
right.pack(side="right", fill="both", expand=True, padx=20, pady=20)

CTkLabel(right, text="Guess the Number", font=("Arial", 20, "bold")).pack(pady=10)

entry = CTkEntry(right, placeholder_text="Enter number", state="disabled")
entry.pack(pady=20, fill="x", padx=40)

CTkButton(right, text="Apply", fg_color="green", command=apply_guess).pack(pady=10)
status_label = CTkLabel(right, text="", font=("Arial", 16))
status_label.pack(pady=10)

points_label = CTkLabel(right, text="Points: 0", font=("Arial", 14))
points_label.pack(pady=10)

CTkButton(right, text="Give Up", fg_color="red", command=give_up).pack(pady=10)
CTkButton(right, text="Admin Mode", fg_color="#444", command=toggle_admin).pack(pady=10)

admin_entry = CTkEntry(right, placeholder_text="6-digit password", show="*")
admin_entry.bind("<Return>", check_admin)
admin_label = CTkLabel(right, text="", font=("Arial", 14))

window.mainloop()
