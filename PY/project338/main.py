import pygame, os, random

pygame.init()

# переменныые под экран и шрифт
screen_x = 1300
screen_y = 700
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Machinki')
font = pygame.font.Font(None, 36)

# подгрузка текстур
road_images = pygame.transform.scale(pygame.image.load(f"{os.path.dirname(__file__)}/background_machinki.png"), (screen_x, screen_y)) # загрузка заднего фона
player_car = pygame.transform.scale(pygame.image.load(f'{os.path.dirname(__file__)}/cars/car1.png'), (50, 100))
bot_car = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f'{os.path.dirname(__file__)}/cars/car2.png'), (50, 100)), 180)
bot_car1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f'{os.path.dirname(__file__)}/cars/car3.png'), (50, 100)), 180)
sprite_health = pygame.transform.scale(pygame.image.load(f'{os.path.dirname(__file__)}/sprite_health.png'), (300, 300))
# в этом блоке загружается картинка изменяется размер и переворачивается в случае спрайтов бота

# позиционные переменные
player_x = 700 # начальные корды игрока 
player_y = 500
bot_y = 100 # начальные корды бота
bot_x = 700
bot_target = 700 # конец пути бота
speed = 30 // 10 # скорость движения(шаг пикселов)
pos = "right" # позиция игрока на полосах(изначально на правой)

# переменные связанные с рандомом
rand_lane = random.randint(0,1) # рандомайзер полосы бота
rand_color = 200 # цвет бота - меняется каждое прохождение пути 
sprite_bots = ['bot_car', 'bot_car1'] # список с переменными спрайтов для бота
rand_bot = random.choice(sprite_bots)

# переменные статистики
score = 0 # так называемый score и health
health = 3

# вспомогательные переменные
game = True # проверка выхода
clock = pygame.time.Clock() # использую для ограничения фпс
anim = False # фалсе - в ожидании нажатия клавиши для запуска игры


while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game = False # закрытие программы при нажатии на крестик
    if event.type == pygame.KEYDOWN: # проверка нажатий клавиш
        anim = True # при нажатии любой клавиши запускается анимация движения ботиков
        match(event.key):
            case(pygame.K_LEFT): # перемещение игрока в левую полосу
                player_x = 550
                pos = 'left'
            case(pygame.K_RIGHT): # перемещение игрока в правую полосу
                player_x = 700
                pos = 'right'    
          
    if anim == True: # если игрок начал игру(нажал хоть одну кнопку)
        if bot_y >= bot_target: # возврат бота наверх и рандомная смена полосы
            rand_bot = random.choice(sprite_bots) # рандомайзер спрайта бота(тут потому что меняется каждый новый цикл перемещения)
            rand_lane = random.randint(0,1) # рандомайзер полосы бота
            score += 1 # +1 к очкам если бот проехал не задев игрока
            bot_y = 0 # перемещение бота на исходную
            if speed <= 18: speed += 1 # ограничение скорости(до 18)
            if rand_lane == 0: # перемещение бота по полосам
                bot_x = 550
            elif rand_lane == 1: 
                bot_x = 700
        elif bot_y < bot_target: # плавное движение к цели
            bot_y += speed
        elif bot_y > bot_target:
            bot_y -= speed


    if bot_y == player_y - 100 or bot_y in range(400, 610): # проверка столкновения с ботом 1
        rand_lane = random.randint(0,1) # рандомайзер полосы бота
        rand_bot = random.choice(sprite_bots) # рандомайзер спрайта бота(тут потому что меняется каждый новый цикл перемещения)
        
        if pos == 'right' and bot_x == 700: # вот такая костыльная пародия на колизию(надо будет сделать через rect кншн)
            if score != 0: score -= 1 # ограничение снижения score
            health -= 1
            bot_y = 10
            if rand_lane == 0:
                bot_x = 550
            elif rand_lane == 1: 
                bot_x = 700
        elif pos == 'left' and bot_x == 550: 
            if score != 0: score -= 1
            health -= 1
            bot_y = 10
            if rand_lane == 0:
                bot_x = 550
            elif rand_lane == 1: 
                bot_x = 700


    screen.blit(road_images, (0, 0)) # чищу прошлый кадр фоном
    text_score = font.render(str(f'Score = {score}'), True, 'red') # обновление score
    text_health = font.render(str(f'Health = {health}'), True, 'red') # обновление health
    screen.blit(text_score, (1000, 50)) # вывод score
    screen.blit(text_health, (1000, 100)) # вывод health

    player = pygame.Rect(player_x, player_y, 50, 100) # параметры игрока и бота
    bot1 = pygame.Rect(bot_x, bot_y, 50, 100 ) # только для колизии

    screen.blit(player_car, (player_x, player_y)) # вывод игрока на экран
    if rand_bot == 'bot_car1': # вывод бота на экран со странной реализацией рандома
        screen.blit(bot_car1, (bot_x, bot_y))
    elif rand_bot == 'bot_car':
        screen.blit(bot_car, (bot_x, bot_y))
    
    if health <= 0: # инструкции при так называемой смерти
        screen.fill('black')
        screen.blit(sprite_health, (screen_x // 2, screen_y // 2))

    pygame.display.flip()
    clock.tick(60) # ограничение на 60 фпс
    
    
    
    