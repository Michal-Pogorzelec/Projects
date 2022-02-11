# Flash Card App - Fiszki
from tkinter import *
import pandas as pd
import random
FONT_1 = ("Arial", 40, "italic")
FONT_2 = ("Arial", 60, "bold")
BACKGROUND_COLOR = "#B1DDC6"

# ------------ Change word on card   ------------ #
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/Fiszki.csv")
    print("File not found.")

# to_learn - lista słowników
to_learn = data.to_dict(orient="records")
current_card = {}


def next_card() -> None:
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfigure(current_img, image=front_card)
    canvas.itemconfigure(Title, text="English", fill="black")
    canvas.itemconfigure(word, text=current_card["English"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card() -> None:
    canvas.itemconfigure(current_img, image=back_card)
    canvas.itemconfigure(Title, text="Polski", fill="white")
    canvas.itemconfigure(word, text=current_card["Polski"], fill="white")


def is_known() -> None:
    global current_card
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ------------ UI ------------ #
window = Tk()
window.title("Fiszki")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
current_img = canvas.create_image(400, 263, image=front_card)
Title = canvas.create_text(400, 150, text="", font=FONT_1)
word = canvas.create_text(400, 263, text="", font=FONT_2)
canvas.grid(row=0, column=0, columnspan=2)

check_image = PhotoImage(file="images/right.png")
right_button = Button(image=check_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

cross_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()


window.mainloop()
