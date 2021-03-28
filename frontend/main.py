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
<<<<<<< HEAD
    shelter_name = ""
    while shelter_name == "":
        shelter_name = input("What is the name of your shelter? ")  
    id_json = requests.get("http://127.0.0.1:5000/api/Login/{name}".format(name=shelter_name)).json()
    id = id_json["data"]["_id"]
    print(id)

=======
    # shelter_name = ""
    # while shelter_name == "":
    #    shelter_name = input("What is the name of your shelter? ") 
    #    requests.get("http://127.0.0.1:5000/api/Login/{name}".format(name=shelter_name))
    
>>>>>>> 5d7d7f32addea11452f47b58fc3da0fc02057cd2
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("VENUS GAME")
    clock = pygame.time.Clock()
    images = load_images()
<<<<<<< HEAD
    buttons = load_buttons()
    
    run_everything = True
    page = "menu"
    while run_everything:
        if page == "menu":
            run_everything, page = menu(page)
        elif page == "options":
            run_everything, page = option(page)
        elif page == "game":
            run_everything, page = main(page)
=======
    main()
>>>>>>> 5d7d7f32addea11452f47b58fc3da0fc02057cd2
