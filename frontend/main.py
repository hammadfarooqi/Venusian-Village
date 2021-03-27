import pygame
import requests
import time
WIDTH,HEIGHT = 1600,900

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

shelterName = ""
if __name__ == '__main__':
    shelter_name = input("What is the name of your shelter? ")
    requests.get("http://127.0.0.1:5000/api/Login/{name}".format(name=shelter_name))
    if(shelterName != ""):
        WIN = pygame.display.set_mode((WIDTH,HEIGHT))
        main()