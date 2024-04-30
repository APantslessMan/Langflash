#################################################
#                   LangFlash                   #
#       A Flash Card Program for learning       #
#                 new languages                 #
#################################################
#################################################
#                   TODO                        #
#################################################
# TODO: get data from web (wiki or git)         #
# TODO: add language selection canvas           #
# TODO: dynamically change language             #
# TODO: save data to proper language locations  #
# TDOD: Change GUI elements, and images         #
#################################################

import random, pandas
from tkinter import *

#################################################
#                   Constants                   #
#################################################
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

#################################################
#                   CSV Import                  #
#################################################


def load_words():
    global data, data_dict

    try:
        data = pandas.read_csv("./data/unknown_words.csv")
    except FileNotFoundError:
        data = pandas.read_csv("./data/french_words.csv")
        data.to_csv('./data/unknown_words.csv', index=False)
    finally:
        data_dict = data.to_dict(orient='records')

#################################################
#                   Functions                   #
#################################################


def next_card():
    global flip_time, current_card
    window.after_cancel(flip_time)
    current_card = random.choice(data_dict)
    canvas.itemconfig(flash_card, image=front_flash)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=f'{current_card["French"]}', fill='black')
    flip_time = window.after(3000, flip_card, current_card)


def know_word():
    print(data_dict)
    print(data.loc[data['French'] == current_card['French']].index[0])
    # drop row from Dataframe, then reload known_words.csv
    data_loc = data.loc[data['French'] == current_card['French']].index[0]
    data.drop(data_loc, axis=0, inplace=True)
    data.to_csv('./data/unknown_words.csv', index=False)
    load_words()
    next_card()


def flip_card(cur_card):
    canvas.itemconfig(flash_card, image=back_flash)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=f'{cur_card["English"]}', fill='white')


#################################################
#                   UI Setup                    #
#################################################

load_words()
window = Tk()
window.title("LangFlash")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_time = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_flash = PhotoImage(file="./images/card_front.png")
back_flash = PhotoImage(file="./images/card_back.png")
flash_card = canvas.create_image(400, 263, image=front_flash)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="title", fill="black", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 260, text="word", fill="black", font=(FONT_NAME, 80, "bold"))

################     Buttons      ###############

yes_image = PhotoImage(file="./images/right.png")
no_image = PhotoImage(file="./images/wrong.png")
yes_button = Button(image=yes_image, highlightthickness=0, command=know_word)
no_button = Button(image=no_image, highlightthickness=0, command=next_card)
yes_button.grid(row=1, column=0)
no_button.grid(row=1, column=1)

next_card()


window.mainloop()
