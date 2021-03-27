import pygame
import requests

WIDTH,HEIGHT = 1600,900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

shelterName = ""
if __name__ == '__main__':
    shelterName = input("What is the name of your shelter? ")  
    if(shelterName != "")
        main()