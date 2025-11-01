import pgzrun
import random
import math
from pygame import Rect

WIDTH = 800
HEIGHT = 480
TITLE = "Sky Runner"

# Estados do jogo
game_state = "menu"
sound_on = True

# Música
music.play("bg_music")
music.set_volume(0.5)

# Classes
class Hero(Actor):
    def __init__(self):
        super().__init__('hero_idle1', (100, HEIGHT - 100))
        self.vy = 0
        self.on_ground = True
        self.frame = 0
        self.images_idle = ['hero_idle1', 'hero_idle2']
        self.images_run = ['hero_run1', 'hero_run2']
        self.anim_timer = 0

    def update(self):
        self.anim_timer += 1
        if keyboard.left or keyboard.right:
            self.frame = (self.frame + 0.1) % len(self.images_run)
            self.image = self.images_run[int(self.frame)]
            if keyboard.left:
                self.x -= 3
                self.angle = 0
            if keyboard.right:
                self.x += 3
        else:
            self.frame = (self.frame + 0.05) % len(self.images_idle)
            self.image = self.images_idle[int(self.frame)]
        self.gravity()

    def gravity(self):
        self.vy += 0.5
        self.y += self.vy
        if self.y >= HEIGHT - 80:
            self.y = HEIGHT - 80
            self.vy = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vy = -10
            self.on_ground = False
            if sound_on:
                sounds.jump.play()

class Enemy(Actor):
    def __init__(self, x, y):
        super().__init__('enemy_run1', (x, y))
        self.images = ['enemy_run1', 'enemy_run2']
        self.frame = 0
        self.direction = random.choice([-1, 1])

    def update(self):
        self.frame = (self.frame + 0.1) % len(self.images)
        self.image = self.images[int(self.frame)]
        self.x += self.direction * 2
        if self.x < 0 or self.x > WIDTH:
            self.direction *= -1

hero = Hero()
enemies = [Enemy(random.randint(400, 700), HEIGHT - 80) for _ in range(3)]

def update():
    global game_state
    if game_state == "menu":
        return
    hero.update()
    for e in enemies:
        e.update()
        if hero.colliderect(e):
            game_state = "menu"
            if sound_on:
                sounds.hit.play()

def draw():
    screen.clear()
    if game_state == "menu":
        screen.draw.text("SKY RUNNER", center=(WIDTH/2, 100), fontsize=60, color="white")
        screen.draw.text("Press ENTER to start", center=(WIDTH/2, 300), fontsize=30)
    else:
        screen.fill((100, 200, 255))
        hero.draw()
        for e in enemies:
            e.draw()

def on_key_down(key):
    global game_state
    if key == keys.RETURN:
        game_state = "game"
    if key == keys.UP:
        hero.jump()

pgzrun.go()