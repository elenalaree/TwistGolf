from tkinter import *
import random
from PIL import Image, ImageTk

root = Tk()
root.title('Twist Golf - Deck')
# root.iconbitmap('')
root.geometry("1500x700")
root.configure(background="green")
discard = []
# Resize cards
def resize_cards(card):
    our_card_img = Image.open(card)

    our_card_resize_img = our_card_img.resize((90, 145))
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_img)
    return our_card_image

# Shuffle cards
def startPile():
    suits = ["diamonds", "clubs", "hearts", "spades"]
    values = range(1, 14)
    # 11 = Jack, 12=Queen, 13=King, 14=Ace

    global deck
    deck =[]

    for suit in suits:
        for value in values:
            deck.append(f'card-{suit}-{value}')
    
    #Create player2s
    global player1, player2
    player1 = []
    player2 = []

    # Grab a random Card
    card = random.choice(deck)
    deck.remove(card)
    # player1 card from deck
    player1.append(card)
    # Output to screen
    global player1_image
    player1_image = resize_cards(f'images/{card}.png')
    player1_label.config(image=player1_image)

    card = random.choice(deck)
    deck.remove(card)
    # player1 card from deck
    player2.append(card)
    # Output to screen
    global player2_image
    player2_image = resize_cards(f'images/{card}.png')
    player2_label.config(image=player2_image)


    root.title(f'Twist Golf - {len(deck)}')

# Draw card
def draw_card():
    try:
        card = random.choice(deck)
        deck.remove(card)
        draw = resize_cards(f'images/{card}.png')
        return draw
    except:
        shuffle_deck()

# shuffle remaining
def shuffle_deck():
    deck = discard

# Deal cards
def deal_cards():
    try:
        # Get the player1 card
        # Grab a random Card
        card = random.choice(deck)
        deck.remove(card)
        # player1 card from deck
        player1.append(card)
        # Output to screen
        global player1_image
        player1_image = resize_cards(f'images/{card}.png')
        player1_label.config(image=player1_image)

        card = random.choice(deck)
        deck.remove(card)
        # player1 card from deck
        player2.append(card)
        # Output to screen
        global player2_image
        player2_image = resize_cards(f'images/{card}.png')
        player2_label.config(image=player2_image)

        root.title(f'Twist Golf - {len(deck)}')

    except:
        root.title(f'Twist Golf - No cards left')

my_frame = Frame(root, bg="green")
my_frame.pack(pady=10)

player1_frame = LabelFrame(my_frame, text="player1", bd=0)
player1_frame.grid(row=0, column=0, ipadx=200,ipady=200, padx=40)

player2_frame = LabelFrame(my_frame, text="player2", bd=0)
player2_frame.grid(row=0, column=2, ipadx=200,ipady=200, padx=40)

player1_label = Label(player1_frame, text='')
player1_label.pack(pady=20)

player2_label = Label(player2_frame, text='')
player2_label.pack(pady=20)

card_back = resize_cards('images/card-back1.png')
center_frame = LabelFrame(my_frame)
center_frame.grid(row=0, column=1, ipadx=80,ipady=40, padx=20)
#Let us create a label for button event
draw_pile_label= Label(image=card_back)




draw_dummy_button = Button(center_frame, image=card_back, command= draw_card,
borderwidth=0)
draw_dummy_button.pack(pady=30)


discard_label = Label(center_frame, text='')
discard_label.pack(pady=10)


startPile()

root.mainloop()