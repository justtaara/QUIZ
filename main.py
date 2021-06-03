#importowanie i inicjowanie pygame
import pygame
from pygame.locals import (KEYUP, K_DOWN, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,) #przyciski
pygame.init()
import time, datetime
from tkinter import *
from random import time
#tworzenie okna gry
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode([screen_width,screen_height])

#Nazwa gry i ikonka
pygame.display.set_caption("Welcome to the jungle")
icon = pygame.image.load("jungle.png") #ikona z flaticon.com, Freepik!
pygame.display.set_icon(icon)

#####GUI#########
def przycisk_koniec():
    pygame.quit()
def przycisk_ponownie():
    pass #jeszcze nie wiem, jak to zrobić
#Grafika - tu wrzucajcie ikonki itp
playerPng = pygame.image.load('lion.png')

#########CZAS##########
timer_stop = datetime.datetime.utcnow() +datetime.timedelta(seconds=90) #SEKUNDY ODLICZANIE - 1,5 minuty

#######GRACZ####### - na razie bez klasy
player_X = int(300)
player_Y = int(300)
player_HP = 90
#zmienne początkowe do ruchu
player_mov_X = int(0)
player_mov_Y = int(0)
#gracz - położenie
#rysowanie gracza
def player_appear():
    screen.blit(playerPng,(int(player_X), int(player_Y)))
    player_box = pygame.Rect(int(player_X), int(player_Y), 35, 40)
    return player_box
#######ROŚLINOŻERCA####### 
class Herbivore():
    def __init__(self):
        self.x = randint(0,500)
        self.y = randint(0,500)
        self.HP = 90 #startowy poziom
        self.mov_X = 0.15
        self.mov_Y = 0.15
    def appear(self):
        herbivorePng = pygame.image.load('monkey.png')
        screen.blit(herbivorePng,(self.x, self.y))
herbivore = Herbivore()
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
#działanie strzałek lub awsd - przyciskanie: (ruch gracza)
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_mov_X = -0.2
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_mov_X = 0.2
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_mov_Y = -0.2
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_mov_Y = 0.2
#działanie strzałek lub awsd - odciśnięcie: (ruch gracza stop)
        if event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_mov_X = 0
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_mov_X = 0
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_mov_Y = 0
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_mov_Y = 0
#gracz nie wchodzi w ściany
    if player_Y <= 0:
        player_Y = 0
    if player_Y >=575:
        player_Y = 575
    if player_X <= 0:
        player_X = 0
    if player_X >= 575:
        player_X = 575
#zielone tło
    screen.fill((127, 255, 0))
#aktualizacja ruchu gracza - początkowa pozycja + zmiana
    player_X += player_mov_X
    player_Y += player_mov_Y
#roślinozerca nie wyjdzie poza ramę + odbije się, jeśli w nią wpadnie
    if herbivore.y <= 0:
        herbivore.mov_Y = 0.15
    if herbivore.y >= 575:
        herbivore.mov_Y = -0.15
    if herbivore.x <= 0:
        herbivore.mov_X= 0.15
    if herbivore.x >= 575:
        herbivore.mov_X = -0.15
    #zmiana położenia roślinożercy
    herbivore.x += herbivore.mov_X
    herbivore.y += herbivore.mov_Y
#pojawienie się gracza na planszy
    player_appear()
#roslinozerca wywolany (na razie 1, pracuję nad tym)
    herbivore.appear()
#koniec pętli
    pygame.display.flip()
pygame.quit()
