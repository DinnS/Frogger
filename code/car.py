from os import walk
import pygame
from random import choice

class Car(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.name = "car"

        self.import_sprite()
        self.image = pygame.image.load(self.full_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.x,self.rect.y)

        if self.rect.x < 200:
            self.direction = pygame.math.Vector2(1,0)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(self.image,True,False)

        self.speed = 300

        # collision
        self.hitbox = self.rect.inflate(0,-self.rect.height / 2)

    def import_sprite(self):
        path_list = list(walk('../graphics/cars'))[0]
        self.full_path = path_list[0] + '/' + choice(path_list[2])


    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.hitbox.center = (round(self.pos.x),round(self.pos.y))
        self.rect.center = self.hitbox.center

        if self.rect.x > 3400 or self.rect.x < -200:
            self.kill()

