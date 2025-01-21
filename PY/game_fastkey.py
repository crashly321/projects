from os import system
import random
from getch import getch

word_list = ['привет', 'пока'] # список слов для игры, пока хз как импортировать их какого нибудь словаря
sentences_list = ['Бу не бойся', 'я друг подойди ко мне']
health = 3 # здоровье игрока
score = 0 # счет игрока 
current_word = random.choice(word_list) # раномное слово из списка
enter_word = 0 # введенное слово
word_quantity = 0 # количество успешно введенных слов

while True: # уровень 1
    system('clear')
    current_word = random.choice(word_list)
    print(f'Ваше здоровье: {health}\nВаш счет: {score}\nТекущее слово: {current_word}')
    enter_word = input('Ввод слова: ')
    if score == 10:
        break
    elif enter_word == current_word:
        score += 1
        word_quantity += 1
    elif enter_word != current_word and health == 1:
        system('clear')
        print(f'Игра окончена, вы проиграли!\nВаш счет: {score}\nПоследнее слово: {current_word}\nКоличество введенных слов: {word_quantity}')
        break
    elif enter_word != current_word:
        health -= 1
system('clear')
print('Поздравляю вы перешли на новый уровень! \nВаш уровень - 2')
input('Введите "продолжить": ')

while True: # уровень 2
    system('clear')
    current_word = random.choice(sentences_list)
    print(f'Ваше здоровье: {health}\nВаш счет: {score}\nТекущее слово: {current_word}')
    enter_word = input('Ввод слова: ')
    if score == 20:
        system('clear')
        print('Харош! Ты прошел эту версию ;)\nВаш счет: {score}\nПоследнее слово: {current_word}\nКоличество введенных слов: {word_quantity}')
        break
    elif enter_word == current_word:
        score += 1
        word_quantity += 1
    elif enter_word != current_word and health == 1:
        system('clear')
        print(f'Игра окончена, вы проиграли!\nВаш счет: {score}\nПоследнее слово: {current_word}\nКоличество введенных слов: {word_quantity}')
        break
    elif enter_word != current_word:
        health -= 1
