from tkinter import *
from tkinter import messagebox
import random
# import pyperclip
import json

# some of functionality won't work, because of images location etc. you need to download it by yourself
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(4, 6)
    nr_symbols = random.randint(1, 2)
    nr_numbers = random.randint(1, 2)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    # "".join(list) zwraca string elementów listy/krotki/słownika oddzielonych sobą ""
    gen_password = "".join(password_list)
    password_input.insert(END, gen_password)

    # automatycznie zapisuje hasło w schowku, gotowe do wklejenia
    # pyperclip.copy(gen_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {website: {
        "email": email,
        "password": password,
        }
    }

    if website != "" and email != "" and password != "":
        try:
            data_file = open(file="data.json", mode="r")
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # wymagane kolejne try, bo w przypadku gdy plik istnieje ale jest pusty, też pojawia się błąd
            try:
                # Reading old data
                data = json.load(data_file)
                # Updating old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            except:
                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(new_data, data_file, indent=4)
        finally:
            data_file.close()
            website_input.delete(0, END)
            password_input.delete(0, END)
    else:
        messagebox.showwarning(title="Warning", message="Don't leave any fields empty!")

# ------------------------- Find Password ----------------------------- #


def find_password():
    website = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="No Data File Found.")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Website: {website}\n"
                                                       f"Email: {data[website]['email']}\n"
                                                       f"Password: {data[website]['password']}")
        else:
            messagebox.showwarning(title="Warning", message="There is no such website in data file.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
# window.minsize(width=300, height=300)
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_input = Entry(width=27)
website_input.focus()
website_input.grid(row=1, column=1)

email_input = Entry(width=45)
email_input.insert(END, "your_email@gmail.com")
email_input.grid(row=2, column=1, columnspan=2)

password_input = Entry(width=27)
password_input.grid(row=3, column=1)

# Buttons
gen_pass_button = Button(text="Generate Password", command=generate_password)
gen_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", width=39, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)


window.mainloop()
