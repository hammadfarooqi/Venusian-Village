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

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path).convert()
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

def load_images():
    images = {}
    images["bg"] = pygame.image.load('images/bg.png').convert()
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
    font = Font("images/large_font.png")
    
    run_everything = True
    page = "menu"
    while run_everything:
        if page == "menu":
            run_everything, page = menu(page)
        elif page == "options":
            run_everything, page = option(page)
        elif page == "game":
            run_everything, page = main(page)
