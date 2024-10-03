from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Label, Button
import random
import os

def load_sprites(folder):
    sprites = {}
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            pokemon_name = filename.split('.')[0]  
            sprites[pokemon_name] = Image.open(os.path.join(folder, filename))
    return sprites

sprites = load_sprites('pokemon_resimler')

def blend_pixels_randomly(pixel1, pixel2, blend_ratio=0.5):
    blended_pixel = tuple(
        int(p1 * blend_ratio + p2 * (1 - blend_ratio))
        for p1, p2 in zip(pixel1, pixel2)
    )
    return blended_pixel

def fuse_pokemon(pokemon1, pokemon2):
    sprite1 = sprites[pokemon1].resize((96, 96)).convert("RGBA")
    sprite2 = sprites[pokemon2].resize((96, 96)).convert("RGBA")

    fused_image = Image.new('RGBA', (96, 96))

    for x in range(96):
        for y in range(96):
            pixel1 = sprite1.getpixel((x, y))
            pixel2 = sprite2.getpixel((x, y))

            if pixel1[3] == 0:  
                fused_image.putpixel((x, y), pixel2)
            elif pixel2[3] == 0:  
                fused_image.putpixel((x, y), pixel1)
            else:
                
                blended_pixel = blend_pixels_randomly(pixel1, pixel2)
                fused_image.putpixel((x, y), blended_pixel)

    return fused_image

def create_fusion_name(pokemon1, pokemon2):
    
    split1 = len(pokemon1) // 2  
    split2 = len(pokemon2) // 2  
    new_name = pokemon1[:split1] + pokemon2[split2:]  
    return new_name.capitalize()

def save_fused_pokemon(pokemon1, pokemon2, save_path):
    fused_image = fuse_pokemon(pokemon1, pokemon2)
    if fused_image:
        fused_image.save(save_path)
    return fused_image

def show_fused_pokemon():
    
    p1, p2 = random.sample(pokemon_list, 2)
    fused_image = save_fused_pokemon(p1, p2, 'fused_pokemon.png')

    
    new_name = create_fusion_name(p1, p2)

    
    fused_image_tk = ImageTk.PhotoImage(fused_image)
    label.config(image=fused_image_tk)
    label.image = fused_image_tk  

    label_text.config(text=f"Fused: {new_name}")  
    original_text.config(text=f"{p1} + {p2}")  

window = tk.Tk()
window.title("Pokémon Fusion")
window.geometry("200x300")

label = Label(window)
label.pack()

original_text = Label(window, text="", font=("Arial", 10))
original_text.pack()

label_text = Label(window, text="Click to fuse Pokémon!", font=("Arial", 12))
label_text.pack()

button = Button(window, text="Fuse Pokémon", command=show_fused_pokemon)
button.pack()

pokemon_list = list(sprites.keys())

window.mainloop()

