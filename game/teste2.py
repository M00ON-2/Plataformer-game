import pgzrun
import math
from pygame import Rect

TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "COLISÃO CORRIGIDA"

plataformas = []
coins = []
obstacles = []

heroi = Actor("heroi", (100, 100))
vel_y = 0
gravidade = 0.5
morto = False


def load_map(caminho):
    with open(caminho, "r") as f:
        linhas = f.read().strip().split("\n")
    for y, linha in enumerate(linhas):
        valores = linha.split(",")
        for x, valor in enumerate(valores):
            if valor in ["21", "22", "23"]:
                imagem = "bloco1"
            elif valor in ["153", "154", "155", "156"]:
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
                coins.append(coin)


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
                obstacles.append(obstacle)


load_map('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
load_coins('C:/Users/PC/Documents/GitHub/roguelike/game/coins.csv')
load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')


def update():
    global vel_y, morto
    if morto:
        return

    # movimento lateral
    if keyboard.left:
        heroi.x -= 3
    if keyboard.right:
        heroi.x += 3

    # gravidade
    vel_y += gravidade
    heroi.y += vel_y

    heroi_rect = Rect(heroi.x - 8, heroi.y - 16, 16, 32)
    no_chao = False

    # --- colisão com plataformas ---
    for bloco in plataformas:
        bloco_rect = Rect(bloco.x - 9, bloco.y - 9, 18, 18)

        # Verifica colisão vertical realista
        if heroi_rect.colliderect(bloco_rect):
            # só para o herói se ele estiver DESCENDO e VINDO DE CIMA
            if vel_y > 0 and heroi.y < bloco.y:
                heroi.y = bloco.y - 18
                vel_y = 0
                no_chao = True

    # pular somente se realmente estiver no chão
    if no_chao and keyboard.up:
        vel_y = -10

    # --- colisão com moedas ---
    for coin in coins[:]:
        coin_rect = Rect(coin.x - 8, coin.y - 8, 16, 16)
        if heroi_rect.colliderect(coin_rect):
            coins.remove(coin)

    # --- colisão com obstáculos ---
    for obstacle in obstacles:
        obstacle_rect = Rect(obstacle.x - 8, obstacle.y - 8, 16, 16)
        if heroi_rect.colliderect(obstacle_rect):
            morto = True
            break


def draw():
    screen.clear()
    for bloco in plataformas:
        bloco.draw()
    for coin in coins:
        coin.draw()
    for obstacle in obstacles:
        obstacle.draw()
    heroi.draw()

    if morto:
        screen.draw.text("VOCÊ MORREU!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=40, color="red", shadow=(1, 1))


pgzrun.go()
