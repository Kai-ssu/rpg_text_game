"""
Created 2 May 2020 
Author: Kye
"""

import requests
import time
import pygame
from pygame.locals import (K_z, K_x, K_c, K_SPACE, QUIT, K_ESCAPE, KEYDOWN)


session = requests.Session()
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 370
FPS = 60

url = 'http://engine.yonapro.webfactional.com/join/?name=kye'
att = 'http://engine.yonapro.webfactional.com/attack/'
stat = 'http://engine.yonapro.webfactional.com/status/'
flee = 'http://engine.yonapro.webfactional.com/flee/'
exp = 'http://engine.yonapro.webfactional.com/explore/'
rest = 'http://engine.yonapro.webfactional.com/rest/'
quit = 'http://engine.yonapro.webfactional.com/quit/'

BLACK = (0, 0, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Goblin Slayer")
clock = pygame.time.Clock()
pygame.mixer.music.load('Lost-Jungle.wav')
pygame.mixer.music.play(-1)

sword = pygame.mixer.Sound("SF-sword-15.wav")
goblin_encounter = pygame.mixer.Sound("goblin-annoyed.wav")
goblin_dead = pygame.mixer.Sound("goblin-dead.wav")
goblin_won = pygame.mixer.Sound("goblin-won.wav")
huh = pygame.mixer.Sound("huh.wav")
gameover = pygame.mixer.Sound("Game_over.wav")

def call(url):
    r = session.get(url)
    if r.status_code == 200:
        res = r.text
        print(res)
        return res
    else:
        return ""

font = pygame.font.SysFont('monosansserif', 110)
small_font = pygame.font.SysFont('monosansserif', 36)


def game_over_screen():
    text = font.render('GAME OVER', True, RED)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH/2, 100)        
    sprite.image.blit(text, text_rect)
    group = pygame.sprite.Group()
    group.add(sprite)
    group.draw(screen)

def go_screen():
    print('GAMEOVER')
    game_over_screen()
    game_over = False
    pygame.mixer.Sound.play(goblin_won)
    pygame.mixer.Sound.play(gameover)
    pygame.mixer.music.stop()

def Dialogue(resp):
    sprite.image.blit(new_forest, sprite.rect)
    response = small_font.render(resp, True, WHITE)
    response_rect = response.get_rect()
    response_rect.center = (SCREEN_WIDTH/2, 250)
    sprite.image.blit(response, response_rect)

def Decision(dec):
    decision = small_font.render(dec, True, WHITE)
    decision_rect = decision.get_rect()
    decision_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    sprite.image.blit(decision, decision_rect)


def status():
    status = small_font.render(call(stat), True, WHITE)
    status_rect = status.get_rect()
    status_rect.center = (110, 340)
    sprite.image.blit(status, status_rect)

forest = pygame.image.load("forest1.gif").convert()
new_forest = forest.copy()

sprite = pygame.sprite.Sprite()
sprite.image = forest
sprite.rect = forest.get_rect()

game_over = True
running = True

Decision(call(url))

while running and game_over:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_z:
                att_res = 'You decided to attack!'
                res = call(att)
                Dialogue(res)
                pygame.mixer.Sound.play(sword)
                l = call(stat)
                life = int(l.split(':')[1].split('/')[0])
                Decision(att_res)
                status()
                if res.find('executes a goblin') >= 0:
                    pygame.mixer.Sound.play(goblin_dead)
                if res.find('feels stronger') >= 0:
                    pygame.mixer.Sound.play(goblin_dead)
                elif res.find('Nothing happens') >= 0:
                    pygame.mixer.Sound.play(goblin_won)
                elif res.find('swats the air, without notable results') >= 0:
                    pygame.mixer.Sound.play(huh)

                if life == 0:
                    go_screen() 
                       
            if event.key == K_x:
                flee_res = 'You decided to flee!'
                res = call(flee)
                Dialogue(res)
                Decision(flee_res)
                status()  

            if event.key == K_c:
                rest_res = 'You decided to rest.'
                res = call(rest)
                Dialogue(res)
                Decision(rest_res)
                status()  
                if res.find('rudely awakened by a goblin') >= 0:
                    pygame.mixer.Sound.play(goblin_encounter)
            if event.key == K_SPACE:
                exp_res = 'You decided to explore.'
                res = call(exp)
                Dialogue(res)
                Decision(exp_res)
                status()
                if res.find('encounters a goblin') >= 0:
                    pygame.mixer.Sound.play(goblin_encounter)
            if event.key == K_ESCAPE:
                running = False
                    
        elif event.type == QUIT:
            running = False

    screen.blit(forest, [0,0])
    pygame.display.flip()

pygame.quit()
    



