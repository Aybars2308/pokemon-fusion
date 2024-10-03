from PIL import Image
from flask import Flask, send_file,request
import random
import os
app = Flask(__name__)

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

def fuse_pokemon(bulbasaur, mewtwo):
    sprite1 = sprites[bulbasaur].resize((96, 96)).convert("RGBA")
    sprite2 = sprites[mewtwo].resize((96, 96)).convert("RGBA")

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

@app.route('/fuse')
def fuse_pokemon_route():
    pokemon1 = request.args.get('p1')
    pokemon2 = request.args.get('p2')
    save_path = "fused_image.png"
    fused_image = fuse_pokemon(pokemon1, pokemon2)
    fused_image.save(save_path)
    return send_file(save_path, mimetype='image/png')

if __name__ == '__main__':
    app.run