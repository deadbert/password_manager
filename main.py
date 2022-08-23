from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_password_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title='Oops', message='please don\'t leave any fields empty!')
    else:
        try:
            with open('data.json', mode='r') as file:
                data = json.load(file)
                data.update(new_password_data)
        except json.decoder.JSONDecodeError:
            with open('data.json', mode='w') as j_file:
                json.dump(new_password_data, j_file, indent=4)
        except FileNotFoundError:
            with open('data.json', mode='w') as j_file:
                json.dump(new_password_data, j_file, indent=4)
        else:
            with open('data.json', mode='w') as j_file:
                json.dump(data, j_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- Search function ------------------------------- #
def search():
    try:
        with open('data.json', 'r') as j_file:
            data = json.load(j_file)
            message_text = f'Email: {data[website_entry.get()]["email"]}\n' \
                           f'Password: {data[website_entry.get()]["password"]}'
            messagebox.showinfo(title=website_entry.get(), message=message_text)
            pyperclip.copy(data[website_entry.get()]["password"])
    except KeyError:
        messagebox.showinfo(title=website_entry.get(), message=f'No entry found for {website_entry.get()}')
    except FileNotFoundError:
        messagebox.showinfo(title=website_entry.get(), message=f'No data file found')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=30, pady=50)

canvas = Canvas(height=200, width=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(84, 100, image=logo, anchor='center')
canvas.grid(column=1, row=0)

website_l = Label(text='Website:')
website_l.grid(column=0, row=1)

email_l = Label(text='Email/Username:')
email_l.grid(column=0, row=2)

password_l = Label(text='Password:')
password_l.grid(column=0, row=3)

website_entry = Entry(width=38)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=48)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, 'example1234@test.com')

password_entry = Entry(width=38)
password_entry.grid(column=1, row=3)

generate_button = Button(text='Generate', command=generate_pass)
generate_button.grid(column=2, row=3)

add_button = Button(text='Add', width=41, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text='Search', width=7, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
