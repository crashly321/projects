import pygame
import os
import time
import random

pygame.init()

screen_x = 1300
screen_y = 700
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Machinki')

font = pygame.font.Font(None, 36)

road_images = pygame.transform.scale(pygame.image.load(f"{os.path.dirname(__file__)}/background_machinki.png"), (screen_x, screen_y)) # загрузка заднего фона

player_x = 700 # начальные корды игрока 
player_y = 500
bot_y = 100 # начальные корды бота
bot_x = 700
bot_target = 700 # конец пути бота
speed = 30 // 10 # скорость движения(шаг пикселов)
score = 0 # так называемый score
pos = "right" # позиция игрока на полосах(изначально на правой)
game = True # проверка выхода
clock = pygame.time.Clock() # хуй пойми надо для ограничения фпс и анимации типо но чет я не пон как мне это использовать(
anim = False # фалсе - в ожидании нажатия клавиши для запуска игры
rand_lane = random.randint(0,1) # рандомайзер полосы бота
rand_color = 200 # цвет бота - меняется каждое прохождение пути 
colors = ['red', 'blue', 'green', 'gray']

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game = False # закрытие программы
    if event.type == pygame.KEYDOWN: # чек нажатий для работы перемещения
        anim = True # при нажатии любой клавиши запускается анимация движения ботиков
        match(event.key):
            case(pygame.K_LEFT): # перемещение игрока в левую полосу
                player_x = 550
                pos = 'left'
            case(pygame.K_RIGHT): # перемещение игрока в правую полосу
                player_x = 700
                pos = 'right'    
          
    if anim == True: # проверка прожатой клавиши
        if bot_y >= bot_target: # возврат бота наверх и рандомная смена полосы
            rand_lane = random.randint(0,1)
            rand_color = random.choice(colors)  #random.randint(100, 200)
            score += 1
            bot_y = 0
            if speed <= 20: speed += 1 
            if rand_lane == 0:
                bot_x = 550
            elif rand_lane == 1: 
                bot_x = 700
        elif bot_y < bot_target: # плавное движение к цели
            bot_y += speed
        elif bot_y > bot_target:
            bot_y -= speed


    if bot_y == player_y - 100 or bot_y in range(400, 610): # проверка столкновения с ботом 1
        rand_lane = random.randint(0,1)
        if pos == 'right' and bot_x == 700: 
            score -= 1
            bot_y = 10
            if rand_lane == 0:
                bot_x = 550
            elif rand_lane == 1: 
                bot_x = 700
        elif pos == 'left' and bot_x == 550: 
            score -= 1
            bot_y = 10
            if rand_lane == 0:
                bot_x = 550
            elif rand_lane == 1: 
                bot_x = 700


    screen.blit(road_images, (0, 0)) # чищу прошлый кадр фоном
    text = font.render(str(f'Score = {score}'), True, 'red') # обновление score
    screen.blit(text, (1000, 50)) # вывод score

    player = pygame.Rect(player_x, player_y, 50, 100) # параметры игрока и бота
    bot1 = pygame.Rect(bot_x, bot_y, 50, 100 )
    pygame.draw.rect(screen, rand_color, bot1, 10) # отрисовка бота
    pygame.draw.rect(screen, (255, 0, 0), player, 10) # отрисовка игрока
                
    pygame.display.flip()
    clock.tick(60)
    
    
    
    