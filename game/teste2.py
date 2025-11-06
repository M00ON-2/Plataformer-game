import pgzrun
import random
import math
from pygame import Rect

TILE_SIZE = 18
ROWS = 30
COLS = 20
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Platformer Adventure"

game_state = "menu"  # "menu", "playing", "dead"
music_on = True
sound_on = True
key_cooldown = 0

platforms = []
obstacles = []
enemies = []




class Hero:
    def __init__(self, x, y):
        self.actor = Actor("hero_idle1", (x, y))
        self.vel_y = 0
        self.gravity = 0.5
        self.dead = False
        self.on_ground = False
        self.frame = 0
        self.anim_timer = 0
        self.state = "idle"

    def rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 16, 16, 32)

    def update(self):
        if self.dead:
            return

        self.handle_input()
        self.apply_gravity()
        self.check_platform_collisions()
        self.animate()

    def handle_input(self):
        move = 0
        if keyboard.left:
            self.actor.x -= 3
            move = -1
        elif keyboard.right:
            self.actor.x += 3
            move = 1

        if self.on_ground and keyboard.up:
            self.vel_y = -10

        if move != 0:
            self.actor.flip_x = move < 0
            self.state = "walk"
        else:
            self.state = "idle"

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.actor.y += self.vel_y

    def check_platform_collisions(self):
        self.on_ground = False
        hero_rect = self.rect()
        for block in platforms:
            block_rect = Rect(block.x - 9, block.y - 9, 18, 18)
            if hero_rect.colliderect(block_rect):
                if self.vel_y > 0 and self.actor.y < block.y:
                    self.actor.y = block.y - 18
                    self.vel_y = 0
                    self.on_ground = True

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 4
            if self.state == "walk":
                self.actor.image = f"hero_walk{self.frame + 1}"
            else:
                self.actor.image = f"hero_idle{self.frame + 1}"

hero = Hero(100, 100)

class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        self.actor = Actor("enemy_idle1", (x, y))
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.direction = 1
        self.frame = 0
        self.anim_timer = 0
        self.state = "walk"

    def rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 8, 16, 16)

    def update(self):
        self.actor.x += self.direction * 2
        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.direction *= -1
        self.animate()

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 4
            self.actor.image = f"enemy_walk{self.frame + 1}"

enemies.append(Enemy(300, 200, 260, 340))
enemies.append(Enemy(500, 150, 460, 560))

def load_map(caminho):
    try:
        with open(caminho, "r") as f:
            linhas = f.read().strip().split("\n")
        for y, linha in enumerate(linhas):
            valores = linha.split(",")
            for x, valor in enumerate(valores):
                if valor in ["21", "22", "23"]:
                    image = "block1"
                elif valor in ["153", "154", "155", "156"]:
                    image = "cloud"
                else:
                    continue
                block = Actor(image)
                block.x = x * TILE_SIZE + TILE_SIZE // 2
                block.y = y * TILE_SIZE + TILE_SIZE // 2
                platforms.append(block)
    except Exception as e:
        print("Erro ao carregar mapa:", e)

load_map("C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv")

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("bg_music")
    else:
        music.stop()

def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        sounds.menu_click.play()

def start_music():
    if music_on:
        music.play("bg_music")

def load_obstacles(caminho):  # carrega os obstáculos
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

load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')


def draw_menu():
    screen.clear()
    screen.draw.text("MAIN MENU", center=(WIDTH//2, 80), fontsize=50, color="white")
    screen.draw.text("1 - Start Game", center=(WIDTH//2, 180), fontsize=40)
    screen.draw.text(f"2 - Music: {'ON' if music_on else 'OFF'}", center=(WIDTH//2, 250), fontsize=40)
    screen.draw.text(f"3 - Sounds: {'ON' if sound_on else 'OFF'}", center=(WIDTH//2, 320), fontsize=40)
    screen.draw.text("4 - Exit", center=(WIDTH//2, 390), fontsize=40)

def update_menu():
    global game_state, key_cooldown
    if key_cooldown > 0:
        key_cooldown -= 1
        return

    if keyboard.K_1:
        if sound_on: sounds.menu_click.play()
        game_state = "playing"
        key_cooldown = 10
    elif keyboard.K_2:
        toggle_music()
        if sound_on: sounds.menu_click.play()
        key_cooldown = 10
    elif keyboard.K_3:
        toggle_sound()
        if sound_on: sounds.menu_click.play()
        key_cooldown = 10
    elif keyboard.K_4:
        if sound_on: sounds.menu_click.play()
        exit()

def update():
    global game_state
    if game_state == "menu":
        update_menu()
        return
    elif game_state == "playing":
        hero.update()
        for enemy in enemies:
            enemy.update()
        check_hero_enemy_collision()

def check_hero_enemy_collision():
    global game_state
    hero_rect = hero.rect()
    for enemy in enemies:
        if hero_rect.colliderect(enemy.rect()):
            hero.dead = True
            game_state = "dead"
            if sound_on: sounds.hit.play()
            break

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
        return
    for block in platforms:
        block.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for enemy in enemies:
        enemy.actor.draw()
    hero.actor.draw()
    if game_state == "dead":
        screen.draw.text("YOU DIED!", center=(WIDTH//2, HEIGHT//2),
                         fontsize=60, color="red", shadow=(2, 2))

start_music()
pgzrun.go()
