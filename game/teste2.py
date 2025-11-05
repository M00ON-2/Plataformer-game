import pgzrun
import math
import random
from pygame import Rect

TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "BOSTAAAAAAAAAAA"

plataformas = []
heroi = Actor("heroi", (100, 100))

def load_map(caminho):
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")

    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor in ["21", "22", "23"]: #terra
                imagem = "bloco1"
            elif valor in ["153", "154", "155", "156"]:  #nuvens
                imagem = "nuvem"
            else:
                continue

            bloco = Actor(imagem)
            bloco.x = x * TILE_SIZE + TILE_SIZE // 2
            bloco.y = y * TILE_SIZE + TILE_SIZE // 2
            plataformas.append(bloco)


def load_coins(caminho):
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")

    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor != "-1":
                coin = Actor("coin")
                coin.x = x * TILE_SIZE + TILE_SIZE // 2
                coin.y = y * TILE_SIZE + TILE_SIZE // 2
                plataformas.append(coin)

def load_obstacles(caminho):
     with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")

     for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor != "-1":
                obstacle = Actor("obstacle")
                obstacle.x = x * TILE_SIZE + TILE_SIZE // 2
                obstacle.y = y * TILE_SIZE + TILE_SIZE // 2
                plataformas.append(obstacle)


load_map('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
load_coins('C:/Users/PC/Documents/GitHub/roguelike/game/coins.csv')
load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')

vel_y = 0
gravidade = 0.5

def update():
    global vel_y

    if keyboard.left:
        heroi.x -= 3
    if keyboard.right:
        heroi.x += 3

    vel_y += gravidade
    heroi.y += vel_y

    heroi_rect = Rect(heroi.x - 16, heroi.y - 16, 32, 32)
    for bloco in plataformas:
        bloco_rect = Rect(bloco.x - 32, bloco.y - 32, 64, 64)
        if heroi_rect.colliderect(bloco_rect) and vel_y >= 0:
            heroi.y = bloco.y - 32
            vel_y = 0
            if keyboard.up:
                vel_y = -10

def draw():
    screen.clear()
    for bloco in plataformas:
        bloco.draw()
    heroi.draw()

pgzrun.go()
