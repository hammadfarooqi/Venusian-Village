import pygame
import requests
import time
import json

WIDTH,HEIGHT = 1152,640

class button():
    def __init__(self, x, y, scale, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/buttons/'+image+'.png').convert()
        self.width = self.image.get_width()*scale
        self.height = self.image.get_height()*scale
        self.show = False
        

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        return False
    
    def draw(self, win):
        if self.show:
            win.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

def clip(surf, x, y, width, height):
    handle_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, width, height)
    handle_surf.set_clip(clip_rect)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class font:
    def __init__(self, path, colors):
        self.text_color = (255, 0, 0)
        self.background_color = (0, 0, 0)
        self.character_order = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-,:+\'!?0123456789()/_=\\[]*"<>;'
        original_font_image = pygame.image.load(path + '.png').convert()
        self.height = original_font_image.get_height()
        current_char_width = 0
        self.color_renders = {}
        for color in colors:
            self.color_renders[color] = {}
            font_image = original_font_image.copy()
            font_image_copy = pygame.Surface(font_image.get_size())
            font_image.set_colorkey(self.text_color)
            font_image_copy.fill(color)
            font_image_copy.blit(font_image, (0, 0))
            font_image_copy.set_colorkey(self.background_color)
            character_count = 0
            for x in range(font_image_copy.get_width()):
                pixel_color = font_image_copy.get_at((x, 0))
                if pixel_color[0] == 127:
                    char_img = clip(font_image_copy, x - current_char_width, 0, current_char_width,
                                    font_image_copy.get_height())
                    self.color_renders[color][self.character_order[character_count]] = char_img.copy()
                    character_count += 1
                    current_char_width = 0
                else:
                    current_char_width += 1

        self.space_width = self.color_renders[colors[0]]['A'].get_width()

    def render(self, surf, text, loc, color, scale=1, spacing=1):
        x_offset = 0
        for char in text:
            if char != ' ':
                self.color_renders[color][char].set_colorkey(self.background_color)
                surf.blit(pygame.transform.scale(self.color_renders[color][char], (self.color_renders[color][char].get_width()*scale, self.color_renders[color][char].get_height()*scale)), (loc[0] + x_offset, loc[1]))
                x_offset += self.color_renders[color][char].get_width()*scale + spacing
            else:
                x_offset += self.space_width*scale + spacing

def load_images():
    images = {}
    images["bg"] = pygame.image.load('images/bg.png').convert()
    images["water"] = pygame.image.load('images/water_drop.png').convert()
    return images

def load_buttons():
    buttons = {}
    buttons["play"] = button(10, 10, 6, "play")
    buttons["options"] = button(10, 20+buttons["play"].height, 6, "options")
    return buttons

def refresh(win, images, buttons, page):
    if page == "game":
        win.blit(pygame.transform.smoothscale(images["bg"], (WIDTH, HEIGHT)), (0, 0))
    else:
        win.fill((100, 100, 50))

    font.render(win, "hello there", (200, 200), (255, 255, 255), 5, 5)
    for button in buttons.values():
        button.draw(win)
    pygame.display.update()

def menu(page):
    buttons["play"].show = True
    buttons["options"].show = True
    
    run_everything = True
    run = True
    while run:
        clock.tick(30)
        refresh(win, images, buttons, page)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run=False
                run_everything = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["play"].isOver(pos) and buttons["play"].show:
                    run = False
                    page = "game"
    buttons["play"].show = False
    buttons["options"].show = False
    return run_everything, page

def main(page):
    run_everything = True
    run = True
    # water = requests.get("http://127.0.0.1:5000/api/Materials/0",params={"materialName":"water"}).json()
    resources = requests.get("http://127.0.0.1:5000/api/Materials/0").json()
    print(type(resources))
    print(resources)
    while run:
        clock.tick(30)
        refresh(win, images, buttons, page)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run=False
                run_everything = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
    return run_everything, page

if __name__ == '__main__':
    shelter_name = ""
    while shelter_name == "":
        shelter_name = input("What is the name of your shelter? ")  
    id_json = requests.get("http://127.0.0.1:5000/api/Login/{name}".format(name=shelter_name)).json()
    # print(id_json)
    id = id_json["data"]["_id"]
    # print(id)

    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Venusian Village")
    clock = pygame.time.Clock()
    images = load_images()
    buttons = load_buttons()
    font = font("images/large_font", [(255, 255, 255)])
    
    run_everything = True
    page = "menu"
    while run_everything:
        if page == "menu":
            run_everything, page = menu(page)
        elif page == "options":
            run_everything, page = option(page)
        elif page == "game":
            run_everything, page = main(page)
