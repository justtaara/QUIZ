#importowanie i inicjowanie pygame
import pygame
from pygame.locals import (KEYUP, K_DOWN, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,) #przyciski
pygame.init()
import time
from tkinter import *
import random

#tworzenie okna gry
screen_width = 600
screen_height = 650
screen = pygame.display.set_mode([screen_width,screen_height])

#Nazwa gry i ikonka
pygame.display.set_caption("Welcome to the jungle")
icon = pygame.image.load("logo.png") #ikona z flaticon.com, Freepik!
pygame.display.set_icon(icon)
#tło gry/mapka dodanie obrazka
jungle_map = pygame.image.load("mapjungle.png")

#####GUI#########
def przycisk_koniec():
    pygame.quit()
def przycisk_ponownie():
    pass #jeszcze nie wiem, jak to zrobić

#########CZAS##########

# Emit an event every second
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)
secs_left = 90

def update_timer():
    "Show the timer in the top-right corner"
    color_white = (255, 255, 255)
    text = str(secs_left).rjust(3)
    rendered_text = font.render(text, True, color_white)
    position = (530, 10)  # decided by trial and error
    screen.blit(rendered_text, position)

#######GRACZ#######
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.mov_X = 0
        self.mov_Y = 0
        self.HP_Player = 100
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('jaguar_main.png')
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.x, self.rect.y)
        self.rect.x = 300
        self.rect.y = 300

    def update(self):
        self.mov_X = 0
        self.mov_Y = 0
        speed = 10
        for event in pygame.event.get():
            if event.type == KEYDOWN:
#działanie strzałek lub awsd - przyciskanie: (ruch gracza)
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.mov_X = - speed
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.mov_X = speed
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    self.mov_Y = -speed
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.mov_Y = speed
#działanie strzałek lub awsd - odciśnięcie: (ruch gracza stop)
            if event.type == KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.mov_X = 0
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.mov_X = 0
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    self.mov_Y = 0
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.mov_Y = 0
        #gracz nie wchodzi w ściany
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >=575:
            self.rect.y = 575
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= 575:
            self.rect.x = 575
        #aktualizacja ruchu gracza - początkowa pozycja + zmiana
        self.rect.x += self.mov_X
        self.rect.y += self.mov_Y

player = Player()

####### ROŚLINOŻERCY I MIĘSOŻERCY #######
class Animal(pygame.sprite.Sprite):
    animal_image = ''
    HP_max = 0
    HP_start = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.animal_image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,565)
        self.rect.y = random.randint(0,565)
        self.HP = self.HP_start  #startowy poziom
        self.health_bar_len = 30
        self.health_ratio = self.HP_max / self.health_bar_len
        self.directions = ['up', 'down','left','right']

    def move(self):
        direction = random.choice(self.directions)
        if direction == "up":
            self.rect.y -= 20
            if self.rect.y <= 10:
                self.rect.y = 10
        elif direction == "down":
            self.rect.y += 20
            if self.rect.y >= 565:
                self.rect.y = 565
        if direction == "left":
            self.rect.x -= 20
            if self.rect.x <= 10:
                self.rect.x = 10
        if direction == "right":
            self.rect.x += 20
            if self.rect.x >= 565:
                self.rect.x = 565

    def use_hp(self):
        self.HP -= 15
        if self.HP <= 0:
            self.kill()

    def update(self):
        self.move()
        self.use_hp()
        self.health_bar()

    def health_bar(self):
        pygame.draw.rect(screen, (255,0,0), ((self.rect.x - 5), (self.rect.y-10), self.HP/self.health_ratio, 10))
        pygame.draw.rect(screen, (255,255,255), ((self.rect.x - 5), (self.rect.y-10), self.health_bar_len,10), 1)

class Herbivore(Animal):
    animal_image = 'monkeys.png'
    HP_max = 900
    HP_start = 800

    def eat_edible_fruit(self, amount):
        if self.HP < self.HP_max:
            self.HP += amount
        if self.HP >= self.HP_max:
            self.HP = self.HP_max
    def eat_inedible_fruit(self, amount):
        if self.HP > 0:
            self.HP -= amount
        if self.HP <= 0:
            self.kill()

class Carnivore(Animal):
    animal_image = 'jaguar_angry.png'
    HP_max = 1500
    HP_start = 500


###### OWOCE ######
#jadalny
class E_Fruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(0, 570)
        self.y = random.randint(0, 570)
        self.image = pygame.image.load('fruit_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,575)
        self.rect.y = random.randint(0,575)
#niejadalny
class I_Fruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(0, 570)
        self.y = random.randint(0, 570)
        self.image = pygame.image.load('fruit_2.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,575)
        self.rect.y = random.randint(0,575)

our_sprites = pygame.sprite.Group() #sprite obsługuje wszystkie poruszające się obiekty w grze #do our_sprites wrzucamy wszystkie poruszające się elementy w grze
herbivores = pygame.sprite.Group() #klasy przedmiotów tworzą osobne grupy
carnivores = pygame.sprite.Group() #klasy przedmiotów tworzą osobne grupy
edible_fruits = pygame.sprite.Group()
inedible_fruits = pygame.sprite.Group()
Player = pygame.sprite.Group()
our_sprites.add(player)

NUM_CARNIVORES = 4


for _ in range(15):
    inedible_fruit = I_Fruit()
    our_sprites.add(inedible_fruit)
    inedible_fruits.add(inedible_fruit)
for _ in range(25):
    edible_fruit = E_Fruit()
    our_sprites.add(edible_fruit)
    edible_fruits.add(edible_fruit)
for _ in range(10):
    herbivore = Herbivore()
    our_sprites.add(herbivore)
    herbivores.add(herbivore)

for _ in range(NUM_CARNIVORES):
    carnivore = Carnivore()
    our_sprites.add(carnivore)
    carnivores.add(carnivore)

#trwanie gry - dopóki gracz jej nie wyłączy, wszystko musi być w pętli!
running = True
while running:
#okienko pojawiające się, kiedy kończy się czas
    if secs_left == 0:
        glowne_okno=Tk()
        glowne_okno.title("Koniec gry!")
        glowne_okno.geometry("250x250")
        text = Text(glowne_okno)
        text.insert(INSERT, "Czas minął, dziękujemy za grę!")
        text.insert(END, "        Twoja punktacja:")
        text.pack()
        przycisk1=Button(glowne_okno, text = "Zakończ", command = przycisk_koniec)
        przycisk1.place(x=30, y= 200)
        przycisk2=Button(glowne_okno, text = "Zagraj ponownie", command = przycisk_ponownie)
        przycisk2.place(x=120, y= 200)
        glowne_okno.mainloop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #wyjście z gry iksem
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #wyjście z gry przyciskiem escape
                running = False
        if event.type == pygame.USEREVENT:
            secs_left -= 1

#update - tło dżungla
    screen.blit(jungle_map , (0,0))
    our_sprites.update() #aktualnie zawiera jedynie chodzenie roślinożerców
    time.sleep(0.2) #opóźnia update, dzięki czemu roślinożercy nie są rozedrgani
    #sprawdzanie czy nie doszło do kolizji
    #jeśli doszło to owoc znika z planszy
    if pygame.sprite.groupcollide(herbivores, edible_fruits, False, True, collided = None):
        herbivore.eat_edible_fruit(60)
    if pygame.sprite.groupcollide(herbivores, inedible_fruits, False, True, collided = None):
        herbivore.eat_inedible_fruit(90)

#gracz się pojawia
    our_sprites.draw(screen)

    update_timer()
#koniec pętli
    pygame.display.flip()
pygame.quit()
