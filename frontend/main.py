import pygame
import requests
import time
import json
from threading import Timer
from random import randint

WIDTH,HEIGHT = 1152,640
root = "http://127.0.0.1:5000/api/"
drain_timer = 15

class button():
    def __init__(self, x, y, scale, image, name = "", price = 0):
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/buttons/'+image+'.png')
        self.width = int(self.image.get_width()*scale)
        self.height = int(self.image.get_height()*scale)
        self.show = False
        self.name = name
        self.price = price

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        return False
    
    def draw(self, win, offset = 0):
        if self.show:
            win.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x + offset, self.y))

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
    images["menu_bg"] = pygame.image.load('images/menu_bg.png').convert()
    images["ui"] = pygame.image.load('images/ui.png')
    
    images["Greenhouse"] = pygame.image.load('images/rooms/Standard_Plant.png')
    images["CloudTreatment"] = pygame.image.load('images/rooms/Sulfuric_Filter.png')
    images["Hospital"] = pygame.image.load('images/rooms/Hospital.png')
    images["Potato"] = pygame.image.load('images/rooms/Spud.png')
    images["Tree"] = pygame.image.load('images/rooms/Tree.png')
    images["RoverDispatch"] = pygame.image.load('images/rooms/Rover.png')
    images["Habitat"] = pygame.image.load('images/rooms/Habitat.png')
    images["Tunnel"] = pygame.image.load('images/rooms/Tunnel.png')
    images["blimp"] = pygame.image.load('images/rooms/Blimp.png')


    return images

def load_buttons():
    buttons = {}
    buttons["play"] = button(200, 400, 1.5, "Play")
    buttons["add_before"] = button(-54, HEIGHT // 2 - 12, 3, "plus")
    buttons["add_after"] = button(0, HEIGHT // 2 - 12, 3, "plus")
    # buttons["options"] = button(10, 20+buttons["play"].height, 6, "options")
    return buttons

def refresh(win, images, buttons, page, rooms =[], x = 0, image_offset = 0, room_cards = [], resources = {}):
    if page == "game":
        win.blit(pygame.transform.smoothscale(images["bg"], (WIDTH, HEIGHT)), (0, 0))
    else:
        win.blit(pygame.transform.smoothscale(images["menu_bg"], (WIDTH, HEIGHT)), (0, 0))

    buttons["add_after"].x=(-94 - (len(rooms)*(224+154)-154 - WIDTH))*-1 + WIDTH - buttons["add_after"].width - 20
    for button in buttons.values():
        button.draw(win, x)
    
    for room_card in room_cards:
        room_card.draw(win)

    for i in range(0, len(rooms)):
        currentRoom = images[rooms[i]['name']]
        win.blit(pygame.transform.scale(currentRoom, (currentRoom.get_width()*2, currentRoom.get_height()*2)), (x, HEIGHT // 2 - currentRoom.get_height()))
        
        win.blit(pygame.transform.scale(images['blimp'], (images['blimp'].get_width()*2, images['blimp'].get_height()*2)), (x+currentRoom.get_width() - images['blimp'].get_width(), HEIGHT // 2 - currentRoom.get_height()-images['blimp'].get_width()*2+50))
        x += currentRoom.get_width()*2 - image_offset
        if i + 1 < len(rooms):
            win.blit(pygame.transform.scale(images["Tunnel"], (images["Tunnel"].get_width()*2, images["Tunnel"].get_height()*2)), (x, HEIGHT // 2 - currentRoom.get_height()))
            x += images["Tunnel"].get_width()*2 - image_offset
    if page == "game":
        win.blit(pygame.transform.smoothscale(images["ui"], (WIDTH, HEIGHT)), (0, 0))
        font.render(win, str(resources["vbucks"]), (1050, 125), (255, 255, 255), scale=2, spacing=2)
        font.render(win, str(resources["population"]), (1060, 565), (255, 255, 255), scale=2, spacing=2)
        resource_per_population = 5
        pygame.draw.rect(win, (0, 255, 0), pygame.Rect(268, 53, int((431 - 268) * resources['water']/(resources['population']*resource_per_population)), 27))
        pygame.draw.rect(win, (0, 255, 0), pygame.Rect(537, 53, int((431 - 268) * resources['food']/(resources['population']*resource_per_population)), 27))
        pygame.draw.rect(win, (0, 255, 0), pygame.Rect(814, 53, int((431 - 268) * resources['oxygen']/(resources['population']*resource_per_population)), 27))
        (431, 82)
    pygame.display.update()

def menu(page):
    buttons["play"].show = True
    # buttons["options"].show = True
    
    run_everything = True
    run = True
    while run:
        clock.tick(30)
        refresh(win, images, buttons, page)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # print(pos)
            if event.type == pygame.QUIT:
                run=False
                run_everything = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["play"].isOver(pos) and buttons["play"].show:
                    run = False
                    page = "game"
    buttons["play"].show = False
    # buttons["options"].show = False
    return run_everything, page
rooms = {}
def habitatClicked(id,name):
    requests.put(root + "ShelterRooms/{id}/{roomName}".format(id=id,roomName=name),params={"value":True})
    print("wow gg")
    rooms = requests.get("http://127.0.0.1:5000/api/Shelters/"+str(id)).json()['data']['rooms']
    print("after request")
def useMaterials(one,two):
    print("TAKING OUT")
    population_per_resource = 5
    population = requests.get(root + "Materials/{id}".format(id=id),params={"materialName":"population"}).json()["data"]
    requests.put(root + "Materials/{id}".format(id=id),params={"materialName":"water", "amount":population // population_per_resource * -1})
    requests.put(root + "Materials/{id}".format(id=id),params={"materialName":"food", "amount":population // population_per_resource * -1})
    requests.put(root + "Materials/{id}".format(id=id),params={"materialName":"oxygen", "amount":population // population_per_resource * -1})

    

    timer = Timer(drain_timer, useMaterials, (1,2))
    timer.start()
    
def main(page):
    buttons["add_before"].show = True
    buttons["add_after"].show = True

    run_everything = True
    run = True
    # water = requests.get("http://127.0.0.1:5000/api/Materials/0",params={"materialName":"water"}).json()
    # print(requests.get("http://127.0.0.1:5000/api/Materials/0"))
    # print(id)
    resources = requests.get(root + "Materials/"+str(id)).json()['data']['materials']
    room = requests.get(root + "Rooms/Habitat").json()["data"]
    requests.put(root + "Shelters/"+str(id), params = {"room":json.dumps(room)})
    rooms = requests.get(root + "Shelters/"+str(id)).json()['data']['rooms']

    add = False
    before = False
    after = False
    
    x_standard = 74
    x = x_standard
    image_offset = 16
    mouse_down = False
    room_buttons = [button(0, HEIGHT // 2 - images[rooms[0]['name']].get_height(), 2, "clear")]
    timer = Timer(drain_timer, useMaterials, (1,2))
    timer.start()
    pos=(0,0)
    while run:
        refresh(win, images, buttons, page, rooms, x, image_offset, room_cards, resources)
        #print(resources)
        resources = requests.get(root + "Materials/"+str(id)).json()['data']['materials']
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run=False
                run_everything = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                room_index = -1
                print("yes")
                for i in range(0, len(room_buttons)):
                    if room_buttons[i].isOver((pos[0]-x, pos[1])):
                        rooms = requests.get(root + "Shelters/"+str(id)).json()['data']['rooms']
                        room_index = i+1
                        # temp fix
                        if room_index == 1:
                            room_index = 2

                        roomClicked = rooms[room_index]
                        if (roomClicked["collectable"]):
                            print(requests.put(root + "ShelterRooms/{id}/{roomName}".format(id=id,roomName=roomClicked["name"]),params={"value":False}))
                            rooms = requests.get(root + "Shelters/"+str(id)).json()['data']['rooms']
                            for resource in roomClicked["resources"]:
                                if(randint(0,100) < roomClicked["errorChance"]):
                                    print("an acid rain storm has happened! The water you were extracting was harmful and hurt your village...")
                                    requests.put(root + "Materials/{id}".format(id=id),params={"materialName":resource, "amount":roomClicked["amount"]*-3})
                                    resources = requests.get(root + "Materials/"+str(id)).json()['data']['materials']
                                else:
                                    print("we're safe")
                                    population_increase_chance = 10
                                    if(randint(0,100) < population_increase_chance):
                                        requests.put(root + "Materials/{id}".format(id=id),params={"materialName":"population", "amount":randint(1,2)})
                                    requests.put(root + "Materials/{id}".format(id=id),params={"materialName":resource, "amount":roomClicked["amount"]})
                                    resources = requests.get(root + "Materials/"+str(id)).json()['data']['materials']
                                    print("made request to add {resource}".format(resource=resource))
                            r = Timer(roomClicked["speed"], habitatClicked, (id,roomClicked["name"]))
                            r.start()
                        else:
                            print("The Room is not ready!")
                if buttons["add_before"].isOver((pos[0]-(x), pos[1])):
                    add = True
                    before = True
                    after = False
                elif buttons["add_after"].isOver((pos[0]-(x), pos[1])):
                    add = True
                    before = False
                    after = True
                else:
                    add = False
                    before = False
                    after = True
                for room_card in room_cards:
                    if room_card.isOver((pos)) and room_card.show and resources['vbucks'] >= room_card.price:
                        if((len(list(filter(lambda room: room["name"] == room_card.name, rooms)))) > 0):
                            break
                        requests.put(root + "Materials/"+str(id),params={"materialName":"vbucks", "amount":-1*room_card.price})
                        resources = requests.get(root + "Materials/"+str(id)).json()['data']['materials']
                        room = requests.get(root + "Rooms/"+room_card.name).json()["data"]
                        requests.put(root + "Shelters/"+str(id), params = {"room":json.dumps(room)})
                        rooms = requests.get(root + "Shelters/"+str(id)).json()['data']['rooms']
                        population_increase_chance = 80
                        if(randint(0,100) < population_increase_chance):
                            requests.put(root + "Materials/{id}".format(id=id),params={"materialName":"population", "amount":randint(1,3)})
                        room_buttons.append(button((images[rooms[i]['name']].get_width()*2 - image_offset+images["Tunnel"].get_width()*2 - image_offset)*len(rooms), HEIGHT // 2 - images[rooms[0]['name']].get_height(), 2, "clear"))
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
        if add:
            for room_card in room_cards:
                room_card.show = True
        else:
            for room_card in room_cards:
                room_card.show = False
        
        if pos[0] < 70:
            x += 10
            if mouse_down:
                x += 10
        elif pos[0] > WIDTH - 70:
            x -= 10
            if mouse_down:
                x -= 10
        if x < -x_standard-20 - (len(rooms)*(224+154)-154 - WIDTH): #Width of images including offset 
            x = -x_standard-20 - (len(rooms)*(224+154)-154 - WIDTH)
        if x > x_standard:
            x = x_standard

        clock.tick(30)
    buttons["add_before"].show = False
    buttons["add_after"].show = False
    for room_card in room_cards:
        room_card.show = False
    return run_everything, page

if __name__ == '__main__':
    shelter_name = ""
    while shelter_name == "":
        shelter_name = input("What is the name of your shelter? ")  
    id_json = requests.get(root + "Login/{name}".format(name=shelter_name)).json()
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
    pygame.mixer.music.load('music/RatsOnVenus.mp3')
    pygame.mixer.music.play(-1)
    room_cards = [button(60, 440, 0.9, "greenhouseRoomCard", "Greenhouse", 300),
    button(60+160, 440, 0.9, "hospitalRoomCard", "Hospital", 200),
    button(60+160*2, 440, 0.9, "potatoRoomCard", "Potato", 200),
    button(60+160*3, 440, 0.9, "roverRoomCard", "RoverDispatch", 300),
    button(60+160*4, 440, 0.9, "treeRoomCard", "Tree", 200),
    button(60+160*5, 440, 0.9, "waterRoomCard", "CloudTreatment", 200)]
    
    run_everything = True
    page = "menu"
    while run_everything:
        if page == "menu":
            run_everything, page = menu(page)
        elif page == "game":
            run_everything, page = main(page)
