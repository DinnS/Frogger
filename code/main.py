import sys
import pygame
from random import choice,randint

from settings import *
from player import Player
from car import Car
from sprite import SimpleSprite,LongSprite

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        # background
        self.bg = pygame.image.load('../graphics/main/map.png').convert()
        self.fg = pygame.image.load('../graphics/main/overlay.png').convert_alpha()

    def customize_draw(self,surface,player_class):
        # change the offset vector
        self.offset.x = player_class.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player_class.rect.centery - WINDOW_HEIGHT / 2

        # blit the background
        surface.blit(self.bg,-self.offset)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            surface.blit(sprite.image, offset_pos)

        surface.blit(self.fg,-self.offset)

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Frogger")

        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.obstacle_sprites = pygame.sprite.Group()

        # Sprites
        self.player = Player((2062,3274),self.all_sprites,self.obstacle_sprites)

        # Timer
        self.car_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.car_timer, 50)
        self.pos_list = []

        # sprite setup
        for file_name,pos_list in SIMPLE_OBJECTS.items():
            sprite_surf = pygame.image.load('../graphics/objects/simple/' + file_name + '.png').convert_alpha()
            for pos in pos_list:
                SimpleSprite(sprite_surf,pos,[self.all_sprites,self.obstacle_sprites])

        for file_name,pos_list in LONG_OBJECTS.items():
            sprite_surf = pygame.image.load('../graphics/objects/long/' + file_name + '.png').convert_alpha()
            for pos in pos_list:
                LongSprite(sprite_surf,pos,[self.all_sprites,self.obstacle_sprites])

        # End screen
        self.font = pygame.font.Font(None,50)
        self.text_surf = self.font.render("You won!",True,'white')
        self.text_rect = self.text_surf.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

        # Music
        self.music = pygame.mixer.Sound("../audio/music.mp3")
        self.music.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.car_timer:
                    random_pos = choice(CAR_START_POSITIONS)
                    if random_pos not in self.pos_list:
                        self.pos_list.append(random_pos)
                        fix_position_car = 40
                        pos = (random_pos[0],random_pos[1] + fix_position_car + randint(-10,10))
                        Car(pos,[self.all_sprites,self.obstacle_sprites])
                    if len(self.pos_list) > 5:
                        del self.pos_list[0]

            self.dt = self.clock.tick() / 1000

            if self.player.pos.y >= 1180:
                # update
                self.all_sprites.update(self.dt)

                # draw
                self.all_sprites.customize_draw(self.display_surface, self.player)
            else:
                self.display_surface.fill('brown')
                self.display_surface.blit(self.text_surf, self.text_rect)

            pygame.display.update()

game = Game()
game.run()