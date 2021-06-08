import random
import pygame

BOARD_SIZE = 575


class Animal:
    caloric_value = 10
    # has to be overriden in subclasses
    animal_image = ''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def appear(self, screen):
        animal_icon = pygame.image.load(self.animal_image)
        screen.blit(animal_icon, (self.x, self.y))

    # Randomly move the animal
    def move(self):
        mu = 0
        sigma = 10

        self.x += random.gauss(mu, sigma)
        self.y += random.gauss(mu, sigma)

        # Make sure that we don't fall out of bounds
        if self.y <= 0:
            self.y = 0
        if self.y >= BOARD_SIZE:
            self.y = BOARD_SIZE
        if self.x <= 0:
            self.x = 0
        if self.x >= BOARD_SIZE:
            self.x = BOARD_SIZE


class Carnivore(Animal):
    animal_image = 'jaguar_angry.png'
    energy_cost = 2

    def __init__(self, x=None, y=None, attack_strength=10, hp=100):
        if x is None:
            x = random.randint(0, BOARD_SIZE)
        if y is None:
            y = random.randint(0, BOARD_SIZE)
        super().__init__(x, y)
        self.hp = hp
        self.attack_strength = attack_strength

    def use_energy(self):
        "Use the energy needed to live"
        self.hp -= self.energy_cost
        self.hp = max(self.hp, 0)

    def eat(self, animal):
        "Eat a carnivore or an omnivore"
        self.hp += animal.caloric_value


