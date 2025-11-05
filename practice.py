from tkinter import Tk, Label, Entry, Button, StringVar
import random
import string

def generate_key(word_input):
    """Generate key according to Variant 7 rules"""
    word = word_input.upper().strip()
    
    if len(word) != 6 or not all(char in string.ascii_letters for char in word):
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

# Create main window
window = Tk()
window.title("Key Generator - Variant 7")
window.geometry('500x300')

# SIMPLE IMAGE LOADING - Replace 'your_image.png' with your actual file name
try:
    from PIL import Image, ImageTk
    image = Image.open("your_image.png")  # CHANGE THIS TO YOUR FILE NAME
    photo = ImageTk.PhotoImage(image)
    
    background_label = Label(window, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = photo  # Keep reference
    
    bg_color = ''
except Exception as e:
    print(f"Image error: {e}")
    window.configure(bg='lightblue')
    bg_color = 'lightblue'

Label(window, text="Variant 7 Key Generator", font=("Arial", 16, "bold"), 
      bg=bg_color if bg_color else 'white').pack(pady=10)

Label(window, text="Enter 6-letter word:", font=("Arial", 12), 
      bg=bg_color if bg_color else 'white').pack()

entry = Entry(window, font=("Arial", 12), width=15, justify='center')
entry.insert(0, 'MASTER')
entry.pack(pady=5)

def generate_press():
    key = generate_key(entry.get())
    result_var.set(key)
    colors = ["red", "green", "yellow", "lightyellow"]
    for i, color in enumerate(colors):
        window.after(i * 100, lambda c=color: result_label.config(bg=c))

generate_btn = Button(window, text="Generate Key", font=("Arial", 12), 
                     command=generate_press, bg="lightgreen")
generate_btn.pack(pady=10)

result_var = StringVar()
result_var.set("XXX-XXXXXX-XXX")

Label(window, text="Generated Key:", font=("Arial", 12), 
      bg=bg_color if bg_color else 'white').pack()

result_label = Label(window, textvariable=result_var, font=("Courier", 14, "bold"), 
                    bg="lightyellow", width=20, relief='sunken')
result_label.pack(pady=10)

instructions = """Format: XXX-XXXXXX-XXX
Block 1: 3 random letters from your word
Block 2: Number positions (A=1,B=2,...)
Block 3: 3 more letters from your word
Example: MASTER -> TMR-319058-AES"""

Label(window, text=instructions, font=("Arial", 9), justify="center",
      bg=bg_color if bg_color else 'white').pack(pady=10)

window.mainloop()