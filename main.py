#importowanie i inicjowanie pygame
import pygame
from pygame.locals import (KEYUP, K_DOWN, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,) #przyciski
pygame.init()
import time
from tkinter import *
from tkinter import messagebox
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
    messagebox.showinfo("Ups!","Niestety, w życiu nie ma drugich szans!")

#okienko kiedy koniec gry nastąpi przez śmierć gracza
def koniec_gry_smierc(self):
    glowne_okno=Tk()
    glowne_okno.title("Koniec gry!")
    glowne_okno.geometry("250x250")
    text = Text(glowne_okno)
    text.insert(INSERT,"Przegrana!                       Niestety, nie masz już HP!")
    text.insert(END, "           Twoja punktacja: " + str(score_value))
    text.pack()
    przycisk1=Button(glowne_okno, text = "Zakończ", command = przycisk_koniec)
    przycisk1.place(x=30, y= 200)
    przycisk2=Button(glowne_okno, text = "Zagraj ponownie", command = przycisk_ponownie)
    przycisk2.place(x=120, y= 200)
    glowne_okno.mainloop()

def koniec_gry_wygrana(self):
    glowne_okno=Tk()
    glowne_okno.title("Koniec gry!")
    glowne_okno.geometry("250x250")
    text = Text(glowne_okno)
    text.insert(INSERT,"Wygrana!                       Wyeliminowano wszystkich wrogów!")
    text.insert(END, "           Twoja punktacja: " + str(score_value))
    text.pack()
    przycisk1=Button(glowne_okno, text = "Zakończ", command = przycisk_koniec)
    przycisk1.place(x=30, y= 200)
    przycisk2=Button(glowne_okno, text = "Zagraj ponownie", command = przycisk_ponownie)
    przycisk2.place(x=120, y= 200)
    glowne_okno.mainloop()
#########CZAS##########

# Emit an event every second
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)
secs_left = 60

def update_timer():
    "Show the timer in the top-right corner"
    color_white = (255, 255, 255)
    text = str(secs_left).rjust(3)
    rendered_text = font.render(text, True, color_white)
    position = (530, 10)  # decided by trial and error
    screen.blit(rendered_text, position)

# punkty gracza
score_value = 0
fonts = pygame.font.SysFont('Consolas', 25)

def show_score():
    score = fonts.render("score:" + str(score_value) , True, (255, 255, 255))
    position_score = (70, 13)
    screen.blit(score, position_score)

# muzyka w tle :)
pygame.mixer.music.load('lamusica.wav') #darmowa muzyka, pobrana z www.dl-sounds.com
pygame.mixer.music.play(-1, 0.0)

# zegar gry
clock = pygame.time.Clock()

#gracz chodzi kiedy trzyma się klawisz
pygame.key.set_repeat(2,3)

#######GRACZ#######
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.mov_X = 0
        self.mov_Y = 0
        self.HP_Player = 1000
        self.HP_Player_Max = 1100
        self.health_bar_len = 30
        self.health_ratio = self.HP_Player_Max / self.health_bar_len
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('jaguar_main.png')
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.x, self.rect.y)
        self.rect.x = 300
        self.rect.y = 300

    def update(self):
        self.mov_X = 0
        self.mov_Y = 0
        speed = 5
        for event in pygame.event.get():
            if event.type == KEYDOWN:
#działanie strzałek lub awsd - przyciskanie: (ruch gracza)
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.mov_X = - speed
                    self.HP_Player -= 5
                    if self.HP_Player <= 0:
                        self.kill()
                        koniec_gry_smierc(self)
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.mov_X = speed
                    self.HP_Player -= 5
                    if self.HP_Player <= 0:
                        self.kill()
                        koniec_gry_smierc(self)
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    self.mov_Y = -speed
                    self.HP_Player -= 5
                    if self.HP_Player <= 0:
                        self.kill()
                        koniec_gry_smierc(self)
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.mov_Y = speed
                    self.HP_Player -= 5
                    if self.HP_Player <= 0:
                        self.kill()
                        koniec_gry_smierc(self)
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
        if self.rect.y <= 50:
            self.rect.y = 50
        if self.rect.y >=575:
            self.rect.y = 575
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= 575:
            self.rect.x = 575

        #health bar gracza
        self.health_bar()

        #aktualizacja ruchu gracza - początkowa pozycja + zmiana
        for i in range(3):
            self.rect.x += self.mov_X
            self.rect.y += self.mov_Y

    def health_bar(self):
        pygame.draw.rect(screen, (102,255,000), ((self.rect.x + 10), (self.rect.y-10), self.HP_Player/self.health_ratio, 10))
        pygame.draw.rect(screen, (255,255,255), ((self.rect.x + 10), (self.rect.y-10), self.health_bar_len,10), 1)

    def HP_up(self):
        self.HP_Player += 50
        if self.HP_Player >= self.HP_Player_Max:
            self.HP_Player = self.HP_Player_Max
    def HP_down(self):
        self.HP_Player -= 100

player = Player()

#######ROŚLINOŻERCA#######
class Herbivore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('monkeys.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,520)
        self.rect.y = random.randint(60,540)
        self.HP = 490 #startowy poziom
        self.HP_max = 500
        self.health_bar_len = 30
        self.health_ratio = self.HP_max / self.health_bar_len
    def update(self):
        player.update()
        self.directionsy = ['up', 'down']
        self.directionsx = ['left','right']
        directiony = random.choice(self.directionsy)
        if directiony == "up":
            self.rect.y -= 10
            self.HP -= 0.25
            if self.HP <= 0:
                self.kill()
            if self.rect.y <= 60:
                self.rect.y = 60
            directionx = random.choice(self.directionsx)
            if directionx == 'left':
                self.rect.x -= 10
                self.HP -= 0.25
                if self.HP <= 0:
                    self.kill()
                if self.rect.x <= 0:
                    self.rect.x = 0
            else:
                self.rect.x += 10
                self.HP -= 0.25
                if self.HP <= 0:
                    self.kill()
                if self.rect.x >= 520:
                    self.rect.x = 520
        else:
            self.rect.y += 10
            self.HP -= 0.25
            if self.HP <= 0:
                self.kill()
            if self.rect.y >= 540:
                self.rect.y = 540
            directionx = random.choice(self.directionsx)
            if directionx == 'left':
                self.rect.x -= 10
                self.HP -= 0.25
                if self.HP <= 0:
                    self.kill()
                if self.rect.x <= 0:
                    self.rect.x = 0
            else:
                self.rect.x += 10
                self.HP -= 0.25
                if self.HP <= 0:
                    self.kill()
                if self.rect.x >= 520:
                    self.rect.x = 520
        self.health_bar()
    def eat_edible_fruit(self, amount):
        print('owocek zjedzony')
        if self.HP < self.HP_max:
            self.HP += amount
        if self.HP >= self.HP_max:
            self.HP = self.HP_max
    def eat_inedible_fruit(self, amount):
        print('małpka została otruta')
        if self.HP > 0:
            self.HP -= amount
        if self.HP <= 0:
            self.kill()
    def health_bar(self):
        pygame.draw.rect(screen, (24, 123, 205), ((self.rect.x + 15), (self.rect.y-10), self.HP/self.health_ratio, 10))
        pygame.draw.rect(screen, (255,255,255), ((self.rect.x + 15), (self.rect.y-10), self.health_bar_len,10), 1)

class Carnivore(pygame.sprite.Sprite):
    animal_image = 'jaguar_angry.png'
    HP_per_turn = 0.25
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.animal_image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,520)
        self.rect.y = random.randint(60,540)
        self.HP = 490 #startowy poziom
        self.HP_max = 500
        self.health_bar_len = 30
        self.health_ratio = self.HP_max / self.health_bar_len

    def update(self):
        self.move_randomly()
        self.HP -= self.HP_per_turn
        if self.HP <= 0:
            self.kill()

        self.health_bar()


    def move_randomly(self):
        directionsy = ['up', 'down']
        directionsx = ['left','right']
        directionx = random.choice(directionsx)
        directiony = random.choice(directionsy)
        if directiony == "up":
            self.rect.y -= 10
            if self.rect.y <= 60:
                self.rect.y = 60
        else:
            self.rect.y += 10
            if self.rect.y >= 540:
                self.rect.y = 540

        if directionx == 'left':
            self.rect.x -= 10
            if self.rect.x <= 0:
                self.rect.x = 0
        else:
            self.rect.x += 10
            if self.rect.x >= 520:
                self.rect.x = 520

    def health_bar(self):
        pygame.draw.rect(screen, (24, 123, 205), ((self.rect.x + 15), (self.rect.y-10), self.HP/self.health_ratio, 10))
        pygame.draw.rect(screen, (255,255,255), ((self.rect.x + 15), (self.rect.y-10), self.health_bar_len,10), 1)

###### OWOCE ######
#jadalny
class E_Fruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('fruit_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,570)
        self.rect.y = random.randint(50,550)
#niejadalny
class I_Fruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('fruit_2.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,570)
        self.rect.y = random.randint(50,550)


player.update()
our_sprites = pygame.sprite.Group() #sprite obsługuje wszystkie poruszające się obiekty w grze #do our_sprites wrzucamy wszystkie poruszające się elementy w grze
herbivores = pygame.sprite.Group() #klasy przedmiotów tworzą osobne grupy
carnivores = pygame.sprite.Group() #klasy przedmiotów tworzą osobne grupy
edible_fruits = pygame.sprite.Group()
inedible_fruits = pygame.sprite.Group()
Player = pygame.sprite.Group()
our_sprites.add(player)

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

NUM_CARNIVORES = 5
for _ in range(NUM_CARNIVORES):
    carnivore = Carnivore()
    our_sprites.add(carnivore)
    carnivores.add(carnivore)


#trwanie gry - dopóki gracz jej nie wyłączy, wszystko musi być w pętli!
running = True
while running:
    score = 0
#okienko pojawiające się, kiedy kończy się czas
    if secs_left == 0:
        glowne_okno=Tk()
        glowne_okno.title("Koniec gry!")
        glowne_okno.geometry("250x250")
        text = Text(glowne_okno)
        text.insert(INSERT, "Czas minął, dziękujemy za grę!")
        text.insert(END, "        Twoja punktacja:" + str(score_value))
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
    our_sprites.update()
    player.update()
    time.sleep(0.2) #opóźnia update, dzięki czemu roślinożercy nie są rozedrgani
    #sprawdzanie czy nie doszło do kolizji
    #jeśli doszło to owoc pojawia się gdzieś indziej
   #groupcollide() przechowuje wyrzucone z planszy elementy i można je ponownie przywołac
    for herbivore in herbivores.sprites():
        eating = pygame.sprite.groupcollide(herbivores,
                                            edible_fruits,
                                            False,
                                            True)
        herbivore.eat_edible_fruit(100)
        for _ in eating:
            fruit = E_Fruit()
            our_sprites.add(fruit)
            edible_fruits.add(fruit)
    for herbivore in herbivores.sprites():
        poisoning = pygame.sprite.groupcollide(herbivores,
                                                inedible_fruits,
                                                False,
                                                True)
        herbivore.eat_inedible_fruit(100)
        for _ in poisoning:
            poison = I_Fruit()
            our_sprites.add(poison)
            inedible_fruits.add(poison)

    our_sprites.draw(screen)

#gracz - funkcje jedzenia
    if pygame.sprite.spritecollide(player, herbivores, True):
        player.HP_up()
        score_value += 10
    if pygame.sprite.spritecollide(player, edible_fruits, True):
        player.HP_up()
        score_value += 1
    if pygame.sprite.spritecollide(player, inedible_fruits, True):
        player.HP_down()
        score_value -= 1

    update_timer()
    show_score()
#koniec pętli
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
