import sys

import pygame
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,collision_sprites):
        super().__init__(groups)

        # image
        self.import_assets()
        self.frame_index = 0
        self.status = 'up'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 300

        # collisions
        self.collisions_sprite = collision_sprites
        self.hitbox = self.rect.inflate(0,-self.rect.height / 2)

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.collisions_sprite.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx # avoid problem with shake screen
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0: # move left
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx  # avoid problem with shake screen
                        self.pos.x = self.hitbox.centerx
        elif direction == 'vertical':
            for sprite in self.collisions_sprite.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery  # avoid problem with shake screen
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery  # avoid problem with shake screen
                        self.pos.y = self.hitbox.centery

    def import_assets(self):
        self.animations = {}
        for index,folder in enumerate(walk('../graphics/player')):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []

            else:
                for file_name in folder[2]:
                    path = folder[0].replace('\\','/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def move(self,dt):
        # Normalize vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal movement + collisions
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # Vertical movement + collisions
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def input(self):
        self.keys = pygame.key.get_pressed()

        # Horizontal input
        if self.keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif self.keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        # Vertical input
        if self.keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif self.keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

    def animate(self,dt):
        self.current_animation = self.animations[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 6 * dt
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = self.current_animation [int(self.frame_index)]

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery


    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()
