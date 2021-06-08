#importowanie i inicjowanie pygame
import pygame
from pygame.locals import (KEYUP, K_DOWN, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,) #przyciski
pygame.init()
import time, datetime
from tkinter import *
import random
from animals import Carnivore

#tworzenie okna gry
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode([screen_width,screen_height])

#Nazwa gry i ikonka
pygame.display.set_caption("Welcome to the jungle")
icon = pygame.image.load("jungle.png") #ikona z flaticon.com, Freepik!
pygame.display.set_icon(icon)
#tło gry/mapka dodanie obrazka
jungle_map = pygame.image.load("mapjungle.png")
#####GUI#########
def przycisk_koniec():
    pygame.quit()
def przycisk_ponownie():
    pass #jeszcze nie wiem, jak to zrobić

#########CZAS##########
timer_stop = datetime.datetime.utcnow() +datetime.timedelta(seconds=90) #SEKUNDY ODLICZANIE - 1,5 minuty

#######GRACZ#######
class Player:
    def __init__(self):
        self.player_X = 300
        self.player_Y = 300
        self.mov_X = 0
        self.mov_Y = 0

    def player_appear(self):
        playerPng = pygame.image.load('jaguar_main.png')
        screen.blit(playerPng,(int(self.player_X), int(self.player_Y)))
        player_box = pygame.Rect(int(self.player_X), int(self.player_Y),int(self.player_X), int(self.player_Y))

    def player_move(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                print('KEYDOWN')
#działanie strzałek lub awsd - przyciskanie: (ruch gracza)
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.mov_X = -20
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.mov_X = 20
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    self.mov_Y = -20
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.mov_Y = 20
        #działanie strzałek lub awsd - odciśnięcie: (ruch gracza stop)
            if event.type == KEYUP:
                print('KEYUP')
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.mov_X = 0
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.mov_X = 0
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    self.mov_Y = 0
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.mov_Y = 0
        #gracz nie wchodzi w ściany
        if self.player_Y <= 0:
            self.player_Y = 0
        if self.player_Y >=575:
            self.player_Y = 575
        if self.player_X <= 0:
            self.player_X = 0
        if self.player_X >= 575:
            self.player_X = 575
        #aktualizacja ruchu gracza - początkowa pozycja + zmiana
        #print(self.mov_X, self.mov_Y)
        self.player_X += self.mov_X
        self.player_Y += self.mov_Y
        #print(self.player_X, self.player_Y)
p = Player()
#######ROŚLINOŻERCA#######
class Herbivore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('monkeys.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,565)
        self.rect.y = random.randint(0,565)
        self.HP = 800  #startowy poziom
        self.HP_max = 900
        self.health_bar_len = 30
        self.health_ratio = self.HP_max / self.health_bar_len
        self.directions = ['up', 'down','left','right']
    def update(self):
        direction = random.choice(self.directions)
        if direction == "up":
            self.rect.y -= 20
            self.HP -= 15
            if self.HP <= 0:
                self.kill()
            if self.rect.y <= 10:
                self.rect.y = 10
        elif direction == "down":
            self.rect.y += 20
            self.HP -= 15
            if self.HP <= 0:
                self.kill()
            if self.rect.y >= 565:
                self.rect.y = 565
        if direction == "left":
            self.rect.x -= 20
            self.HP -= 15
            if self.HP <= 0:
                self.kill()
            if self.rect.x <= 10:
                self.rect.x = 10
        if direction == "right":
            self.rect.x += 20
            self.HP -= 15
            if self.HP <= 0:
                self.kill()
            if self.rect.x >= 565:
                self.rect.x = 565
        self.health_bar()
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
    def health_bar(self):
        pygame.draw.rect(screen, (255,0,0), ((self.rect.x - 5), (self.rect.y-10), self.HP/self.health_ratio, 10))
        pygame.draw.rect(screen, (255,255,255), ((self.rect.x - 5), (self.rect.y-10), self.health_bar_len,10), 1)
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
        
NUM_CARNIVORE = 4
carnivores = []
for i in range(NUM_CARNIVORE):
    carnivores.append(Carnivore())

our_sprites = pygame.sprite.Group() #sprite obsługuje wszystkie poruszające się obiekty w grze #do our_sprites wrzucamy wszystkie poruszające się elementy w grze
herbivores = pygame.sprite.Group() #klasy przedmiotów tworzą osobne grupy
edible_fruits = pygame.sprite.Group()
inedible_fruits = pygame.sprite.Group()
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
#trwanie gry - dopóki gracz jej nie wyłączy, wszystko musi być w pętli!
running = True
while running:
#okienko pojawiające się, kiedy kończy się czas
    if datetime.datetime.utcnow() > timer_stop:
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

#zielone tło 
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
    p.player_appear()
    p.player_move()
    our_sprites.draw(screen) 
    for carnivore in carnivores:
        carnivore.move()
        carnivore.appear(screen)

#koniec pętli
    pygame.display.flip()
pygame.quit()

