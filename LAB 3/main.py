from tkinter import Tk, Label, Entry, Button, StringVar, PhotoImage
import random
import string
import pygame # type: ignore


def generate_key(word_input):
    """Generate key according to Variant 7 rules."""
    word = word_input.upper().strip()
    
    if len(word) != 6 or not all(
            char in string.ascii_letters for char in word):
        return "ERROR: Need 6 letters"
    
    block1 = ''.join(random.sample(word, 3))
    
    block2 = ''
    for letter in word:
        position = ord(letter) - ord('A') + 1
        units_digit = position % 10
        block2 += str(units_digit)
    
    remaining_letters = [c for c in word if c not in block1]
    if len(remaining_letters) >= 3:
        block3 = ''.join(random.sample(remaining_letters, 3))
    else:
        block3 = ''.join(random.sample(word, 3))
    
    key = f"{block1}-{block2}-{block3}"
    return key


def main():
    pygame.mixer.init()
    pygame.mixer.music.load("Hans Zimmer - Eternal Honor (hitmos.fm).mp3") 
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    window = Tk()
    window.title("Key Generator - Variant 7")
    window.geometry('500x300')
    
    bg_image = PhotoImage(file="call of duty-ghost.png")
    bg_label = Label(window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    title_label = Label(
        window, 
        text="Variant 7 Key Generator", 
        font=("Arial", 16, "bold"), 
        bg='white'
    )
    title_label.pack(pady=10)
    
    input_label = Label(
        window, 
        text="Enter 6-letter word:", 
        font=("Arial", 12), 
        bg='white'
    )
    input_label.pack()
    
    entry = Entry(window, font=("Arial", 12), width=15, justify='center')
    entry.insert(0, 'MASTER')
    entry.pack(pady=5)
    
    def generate_press():
        """Handle generate button press."""
        key = generate_key(entry.get())
        result_var.set(key)
        
        colors = ["red", "green", "yellow", "lightyellow"]
        for i, color in enumerate(colors):
            window.after(i * 100, lambda c=color: result_label.config(bg=c))
    
    generate_btn = Button(
        window,
        text="Generate Key",
        font=("Arial", 12),
        command=generate_press,
        bg="lightgreen"
    )
    generate_btn.pack(pady=10)
    
    result_var = StringVar()
    result_var.set("XXX-XXXXXX-XXX")
    
    result_text_label = Label(
        window,
        text="Generated Key:",
        font=("Arial", 12),
        bg='white'
    )
    result_text_label.pack()
    
    result_label = Label(
        window,
        textvariable=result_var,
        font=("Courier", 14, "bold"),
        bg="lightyellow",
        width=20,
        relief='sunken'
    )
    result_label.pack(pady=10)
    
    window.mainloop()


if __name__ == "__main__":
    main()