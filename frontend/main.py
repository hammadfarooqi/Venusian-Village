import pygame
import requests
import time

WIDTH,HEIGHT = 1152,640
    

def load_images():
    images = {}
    images["bg"] = pygame.image.load('images/bg.png').convert()
    return images


def refresh(images):
    win.blit(pygame.transform.smoothscale(images["bg"], (WIDTH, HEIGHT)), (0, 0))
    pygame.display.update()

def main():
    run = True
    while run:
        clock.tick(30)
        refresh(images)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

shelter_name = ""
if __name__ == '__main__':
    # shelter_name = ""
    # while shelter_name == "":
    #    shelter_name = input("What is the name of your shelter? ") 
    #    requests.get("http://127.0.0.1:5000/api/Login/{name}".format(name=shelter_name))
    
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("VENUS GAME")
    clock = pygame.time.Clock()
    images = load_images()
    main()
