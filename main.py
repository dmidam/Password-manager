from tkinter import *
from tkinter import messagebox
import random
import json
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    letters_add = [password_list.append(random.choice(letters)) for let in range(nr_letters)]
    symbols_add = [password_list.append(random.choice(symbols)) for sym in range(nr_symbols)]
    numbers_add = [password_list.append(random.choice(numbers)) for num in range(nr_numbers)]

    random.shuffle(password_list)

    password_print = "".join(password_list)
    password_entry.insert(0, password_print)
    pyperclip.copy(password_print)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    web = website_entry.get()
    mail = email_user_entry.get()
    passw = password_entry.get()
    new_data = {
        web: {
            "mail": mail,
            "password": passw,
        }
    }

    if len(web) == 0 or len(passw) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data:
                # Reading old data
                # json.dump(new_data, data, indent=4)
                data_file = json.load(data)
                # Updating old data with new data
                data_file.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data:
                json.dump(new_data, data, indent=4)
        else:
            with open("data.json", "w") as data:
                # Saving updated data
                json.dump(data_file, data, indent=4)
        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")
            website_entry.focus()

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            if website_entry.get() in data:
                messagebox.showinfo(title=f"{website_entry.get()}",
                                    message=f"Email: {data[website_entry.get()]['mail']}\n"
                                            f"Password: {data[website_entry.get()]['password']}")
            else:
                messagebox.showinfo(title=f"{website_entry.get()}", message="No details for the website exists.")
    except FileNotFoundError:
        messagebox.showinfo(title=f"{website_entry.get()}", message="No Data File Found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)
# image

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
website = Label(text="Website:")
website.grid(column=0, row=1)
email_user = Label(text="Email/Username:")
email_user.grid(column=0, row=2)
password = Label(text="Password:")
password.grid(column=0, row=3)

# Entries
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()
email_user_entry = Entry(width=35)
email_user_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_user_entry.insert(0, "test@gmail.com")
password_entry = Entry(width=35)
password_entry.grid(column=1, row=3, sticky="W")

# Buttons
generate_password = Button(text="Generate Password", command=generate_password)
generate_password.grid(column=2, row=3, sticky="EW")
add = Button(text="Add", width=36, command=save)
add.grid(column=1, row=4, columnspan=2, sticky="EW")
search = Button(text="Search", width=20, command=find_password)
search.grid(column=2, row=1, sticky="EW")


window.mainloop()
