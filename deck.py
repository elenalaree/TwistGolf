from tkinter import *
import random
from PIL import Image, ImageTk
import pygame

root = Tk()
root.title('Twist Golf - Deck')
# root.iconbitmap('')
root.geometry("1500x400")
root.configure(background="green")
pygame.mixer.init()

discard = []
player1_card_flipped = [False] * 6
player2_card_flipped = [False] * 6
my_frame = Frame(root, bg="green")
my_frame.pack(pady=10)

player1_frame = LabelFrame(my_frame, text="Player 1", bd=0, bg="green")
player1_frame.grid(row=0, column=0, ipadx=200, ipady=200, padx=40)

player2_frame = LabelFrame(my_frame, text="Player 2", bd=0, bg="green")
player2_frame.grid(row=0, column=2, ipadx=200, ipady=200, padx=40)
# card flip sound
def flip_card_sound():
    pygame.mixer.music.load("sounds/flipcard-91468.mp3")
# Resize cards
def resize_cards(card):
    our_card_img = Image.open(card)

    our_card_resize_img = our_card_img.resize((90, 145))
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_img)
    return our_card_image

pileTop = 'card-blank'

discardStart = resize_cards(f'images/{pileTop}.png')
card_back = resize_cards('images/card-back1.png')
# Create lists to store images and buttons for player 1 and player 2 cards
player1_image = [card_back] * 6
player1_card = [card_back] * 6
player2_image = [card_back] * 6
player2_card = [card_back] * 6

# reset flip State
def fix_commands():
    for j in range(6):
        if not player1_card_flipped[j]:
            print(f'Assigning flipCard command to player1 index-{j}')
            player1_card[j].config(command=lambda j=j: flipCard(1, j))
        else:
            print(f'Player1 index-{j} is flipped, removing command')
            player1_card[j].config(command='')

        if not player2_card_flipped[j]:
            print(f'Assigning flipCard command to player2 index-{j}')
            player2_card[j].config(command=lambda j=j: flipCard(2, j))
        else:
            print(f'Player2 index-{j} is flipped, removing command')
            player2_card[j].config(command='')

    print('Assigning discard_prep command to discard_dummy_button')
    discard_dummy_button.config(command=discard_prep)

# Refresh card on top
def get_discard():
    global pileTop_image, pileTop
    pileTop_image = resize_cards(f'images/{pileTop}.png')
    discard_dummy_button.config(image=pileTop_image)

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

    # Grab 6 random Cards for player 1
    player1 = random.sample(deck, 6)
    for card in player1:
        deck.remove(card)

    player2 = random.sample(deck, 6)
    for card in player2:
        deck.remove(card)

    print(player1, player2)

    global discard
    card = random.choice(deck)
    deck.remove(card)
    discard.append(card)
    
    global pileTop
    pileTop = discard[-1]
    
    get_discard()
    root.title(f'Twist Golf - {len(deck)}')


# Draw card
def draw_card():
    try:
        card = random.choice(deck)
        deck.remove(card)
        draw = resize_cards(f'images/{card}.png')
        drawn_card_button.config(image=draw)

# Enable clicking on player cards or discard pile to make a choice
        for i in range(6):
            player1_card[i].config(command=lambda i=i: draw_card_choice(1, i, card))
            player2_card[i].config(command=lambda i=i: draw_card_choice(2, i, card))
        discard_dummy_button.config(command=lambda: draw_card_choice(0, 0, card))
    
        root.title(f'Twist Golf - {len(deck)}')
    except:
        shuffle_deck()


# Player choice
def draw_card_choice(self, i, draw):
    global player1_image, player2_image, discard, player1, player2, pileTop
    
    if(self == 0):
        discard.append(draw)
    if(self == 1):
        clicked_card = player1[i]
        discard.append(player1[i])
        player1[i] = draw
        print(f'PileTop Card: {pileTop}')
        print(f'Clicked Card: {clicked_card}')
        
        player1_image[i] = resize_cards(f'images/{draw}.png')
        player1_card[i].config(image=player1_image[i])
        player1_card_flipped[i] = True

    elif(self == 2):
        clicked_card = player2[i]
        discard.append(player2[i])
        player2[i] = draw
        print(f'PileTop Card: {pileTop}')
        print(f'Clicked Card: {clicked_card}')
        
        player2_image[i] = resize_cards(f'images/{draw}.png')
        player2_card[i].config(image=player2_image[i])
        player2_card_flipped[i] = True
    pileTop = discard[-1]
    get_discard()
    fix_commands()
    if(all(player1_card_flipped) or all(player2_card_flipped)):
        print("Game over!")
    

def discard_prep():
    for j in range(6):
        player1_card[j].config(command=lambda j=j: discard_pile_choice(1, j))
        player2_card[j].config(command=lambda j=j: discard_pile_choice(2, j))
        


def discard_pile_choice(player, i):
    global player1_image, player2_image, discard, player1, player2, pileTop
    draw = pileTop
    if(player == 1):
        clicked_card = player1[i]
        discard.append(player1[i])
        player1[i] = pileTop
        player1_image[i] = resize_cards(f'images/{draw}.png')
        player1_card[i].config(image=player1_image[i])

    elif(player == 2):
        clicked_card = player2[i]
        discard.append(player2[i])
        player2[i] = pileTop
        print(f'PileTop Card: {pileTop}')
        print(f'Clicked Card: {clicked_card}')
        player2_image[i] = resize_cards(f'images/{draw}.png')
        player2_card[i].config(image=player2_image[i])
    pileTop = discard[-1]
    get_discard()
    fix_commands()
    if(all(player1_card_flipped) or all(player2_card_flipped)):
        print("Game over!")
    print(player1, player2)


# Flip card
def flipCard(player, index):
    # take the player and card info to create the card
    global player1_image, player2_image, player1_card_flipped, player2_card_flipped

    if player == 1:
        card = player1[index]
        player1_image[index] = resize_cards(f'images/{card}.png')
        player1_card[index].config(image=player1_image[index])
        player1_card_flipped[index] = True
    elif player == 2:
        card = player2[index]
        player2_image[index] = resize_cards(f'images/{card}.png')
        player2_card[index].config(image=player2_image[index])
        player2_card_flipped[index] = True
    flip_card_sound()
    if(all(player1_card_flipped) or all(player2_card_flipped)):
        print("Game over!")
    print(f"Flipped player {player}'s {card} index")


# shuffle remaining
def shuffle_deck():
    global deck, discard
    deck = discard
    discard = []




# Player 1 cards
player1_label1 = Label(player1_frame, image=card_back)
player1_card[0] = Button(player1_frame, image=card_back, command=lambda: flipCard(1, 0), borderwidth=0)
player1_card[0].place(x=50, y=10)

player1_label2 = Label(player1_frame, image=card_back)
player1_card[1] = Button(player1_frame, image=card_back, command=lambda: flipCard(1, 1), borderwidth=0)
player1_card[1].place(x=150, y=10)

player1_label3 = Label(player1_frame, image=card_back)
player1_card[2] = Button(player1_frame, image=card_back, command=lambda: flipCard(1, 2), borderwidth=0)
player1_card[2].place(x=250, y=10)

player1_label4 = Label(player1_frame, image=card_back)
player1_card[3] = Button(player1_frame, image=card_back, command=lambda: flipCard(1, 3), borderwidth=0)
player1_card[3].place(x=50, y=175)

player1_label5 = Label(player1_frame, image=card_back)
player1_card[4] = Button(player1_frame, image=card_back, command=lambda: flipCard(1, 4), borderwidth=0)
player1_card[4].place(x=150, y=175)

player1_label6 = Label(player1_frame, image=card_back)
player1_card[5] = Button(player1_frame, image=card_back, command=lambda: flipCard(1, 5), borderwidth=0)
player1_card[5].place(x=250, y=175)

# Player 2 cards
player2_label1 = Label(player2_frame, image=card_back)
player2_card[0] = Button(player2_frame, image=card_back, command=lambda: flipCard(2, 0), borderwidth=0)
player2_card[0].place(x=50, y=10)

player2_label2 = Label(player2_frame, image=card_back)
player2_card[1] = Button(player2_frame, image=card_back, command=lambda: flipCard(2, 1), borderwidth=0)
player2_card[1].place(x=150, y=10)

player2_label3 = Label(player2_frame, image=card_back)
player2_card[2] = Button(player2_frame, image=card_back, command=lambda: flipCard(2, 2), borderwidth=0)
player2_card[2].place(x=250, y=10)

player2_label4 = Label(player2_frame, image=card_back)
player2_card[3] = Button(player2_frame, image=card_back, command=lambda: flipCard(2, 3), borderwidth=0)
player2_card[3].place(x=50, y=175)

player2_label5 = Label(player2_frame, image=card_back)
player2_card[4] = Button(player2_frame, image=card_back, command=lambda: flipCard(2, 4), borderwidth=0)
player2_card[4].place(x=150, y=175)

player2_label6 = Label(player2_frame, image=card_back)
player2_card[5] = Button(player2_frame, image=card_back, command=lambda: flipCard(2, 5), borderwidth=0)
player2_card[5].place(x=250, y=175)


# Center console and draw station
center_frame = LabelFrame(my_frame)
center_frame.grid(row=0, column=1, ipadx=100,ipady=200, padx=20)
#Let us create a label for button event
draw_pile_label= Label(image=card_back)

# Drawn card button
drawn_card_button = Button(center_frame, image=card_back, command=draw_card_choice, borderwidth=0)
drawn_card_button.place(x=50, y=0)

# Discard pile button
discard_dummy_button = Button(center_frame, image=discardStart, command=discard_prep, borderwidth=0)
discard_dummy_button.place(x=0, y=200)

draw_dummy_button = Button(center_frame, image=card_back, command=draw_card,
borderwidth=0)
draw_dummy_button.place(x=105, y=200)




startPile()

root.mainloop()