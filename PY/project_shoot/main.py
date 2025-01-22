import pygame
import os
import time
import random
import settings

from abc import ABC, abstractmethod

pygame.init()

screen = pygame.display.set_mode((settings.screen_x, settings.screen_y))
pygame.display.set_caption(settings.window_name)
game = True
clock = pygame.time.Clock()

game_score = 0

'''
Делаю 3 класса:
    1 - пушка, в виде ровного треугольника из середины будет вылетать снаряд
    2 - снаряд, вид круглика, скорость, цвет, движение(достану кусок кода с плавным движением из машинок), 
        стрельба по кнопке
    3 - цель, движущийся прямоугольник, так же скорость, должна ездить в пределах окошка
        (мб изменить скорость на минусовую при достижении screen_x), при попадании становится красной и прибавляет score
Фон звездный какой нибудь в инете высрать

'''
background = pygame.image.load(f'{os.path.dirname(__file__)}/star_back.jpg')
font = pygame.font.Font(None, 36)

objects = []

class object:
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.collider = pygame.Rect(0, 0, 0, 0)
        self.tag = "object"

    @abstractmethod
    def update(self, deltaTime):
        pass

    @abstractmethod
    def draw(self):
        pass

    def check_collider(self, object: pygame.Rect):
        return self.collider.colliderect(object)
    
class gun(object):
    def __init__(self):
        self.posX = 320
        self.posY = 450
        self.tag = "gun"

        self.collider = pygame.Rect(self.posX, self.posY, 10, 10)

    def update(self, deltaTime):
        self.collider.left = self.posX - 5
        self.collider.top = self.posY - 5

        self.posY -= 5
        if self.posY <= 0:
            objects.remove(self)
            objects[0].gun = None   
        
    def draw(self):
        pygame.draw.polygon(screen, 'red', ((self.posX - 5, self.posY), (self.posX, self.posY - 5), (self.posX + 5, self.posY)), width=5)
        pygame.draw.rect(screen, (250, 0, 0), self.collider, 10)

class space_bot(object):
    def __init__(self):
        self.posX = 320
        self.posY = 350
        self.sprite_ship = pygame.image.load(f'{os.path.dirname(__file__)}/space_ship.png')
        self.sprite_ship_small = pygame.transform.scale(self.sprite_ship, (50, 100))
        self.gun = None
        self.strike = 0

        self.tag = "player"
        self.collider = pygame.Rect(self.posX, self.posY, 50, 100)

    def update(self, deltaTime):
        global game_score

        if len(objects) > 1:
            self.botposY = objects[1].posY
            self.botposX = objects[1].posX

        self.collider.left = self.posX
        self.collider.top = self.posY

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.posX >= 0:
            self.posX -= 10
        elif keys[pygame.K_d] and self.posX <= settings.screen_x - 50:
            self.posX += 10

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.posX >= 0:
                self.posX -= 10
            elif event.key == pygame.K_RIGHT and self.posX <= settings.screen_x - 50:
                self.posX += 10

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and self.gun == None:
            self.gun = gun()
            self.gun.posX = self.posX + 25
            self.gun.posY = self.posY - 15
            objects.append(self.gun)
            
            if self.gun.posY == self.botposY - 100 and self.gun.posX in range(self.botposX - 25, self.botposX + 25):
                objects.remove(self)
                objects[0].gun = None
                game_score += 1
                print('suda')


    def draw(self):
        screen.blit(self.sprite_ship_small, (self.posX, self.posY))
        pygame.draw.rect(screen, (250, 0, 0), self.collider, 10)

class animals(object):
    def __init__(self):
        self.sprite_bot = objects[0].sprite_ship_small
        self.sprite_bot = pygame.transform.rotate(self.sprite_bot, 180)
        self.posY = 10
        self.posX = 290
        self.tag = "animals"

        self.collider = pygame.Rect(self.posX, self.posY, 50, 100)

    def update(self, deltaTime):
        global game_score

        self.collider.left = self.posX
        self.collider.top = self.posY

        if self.posY <= settings.screen_y:
            self.posY += 3
            if self.posY >= settings.screen_y:
                self.posY = 3
                self.posX = random.randint(10, 600)
                print('cray', self.posY)
        '''
        if self.posY >= 270 and self.posX in range(playerposX-25, playerposX+25):
            self.posY = 3
            self.posX = random.randint(10, 600)
            self.score -= 1
            print('stolk', self.posY)
        '''
        if self.check_collider(objects[0].collider):
            self.posY = 3
            self.posX = random.randint(10, 600)
            game_score -= 1
            print('stolk', self.posY)

        all_bullet = list(filter(lambda x: x.tag == "gun", objects))
        
        if all_bullet and self.check_collider(all_bullet[0].collider):
            objects.remove(self)
            objects[0].gun = None
            game_score += 1
            print('suda')

    def draw(self):
        screen.blit(self.sprite_bot, (self.posX, self.posY))
        pygame.draw.rect(screen, (250, 0, 0), self.collider, 10)
        

objects.append(space_bot()) # Player
objects.append(animals()) # Bot

last_time = pygame.time.get_ticks() 

while game:
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - last_time) / 1000.0  # Время в секундах
    last_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT: game = False # закрытие программы
    if event.type == pygame.KEYDOWN: 
        match(event.key):
            case(pygame.K_0): 
                pass
    
    screen.blit(background, (0, 0))
    
    for obj in objects:
        obj.update(last_time)
        obj.draw()

    text = font.render(str(f'Score = {game_score}'), True, 'red')
    screen.blit(text, (50, 400))

    pygame.display.flip()
    clock.tick(60)


