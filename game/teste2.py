import pgzrun; from pygame import Rect

TILE_SIZE, ROWS, COLS = 18, 30, 20
WIDTH, HEIGHT = TILE_SIZE * ROWS, TILE_SIZE * COLS
TITLE = "Cloud Parkour Refatorado"

platforms = []

class CharacterBase: # ! PRINCIPAL CLASSE
    def __init__(self, image, pos, gravity=0.5, speed=2):
        self.actor = Actor(image, pos)
        self.vel_y = 0
        self.gravity = gravity
        self.speed = speed
        self.frame = 0
        self.anim_timer = 0
        self.state = "idle"
        self.on_ground = False
        self.dead = False
        self.direction = 1  # 1 = direita, -1 = esquerda

    def rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 16, 16, 32)

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.actor.y += self.vel_y

    def check_platform_collisions(self):
        self.on_ground = False
        hr = self.rect()
        for b in platforms:
            br = Rect(b.x - 9, b.y - 9, 18, 18)
            if hr.colliderect(br) and self.vel_y > 0 and self.actor.y < b.y:
                self.actor.y = b.y - 18
                self.vel_y = 0
                self.on_ground = True
                
    def animate(self, prefix):
        self.anim_timer += 1
        if self.anim_timer > 8:
         self.anim_timer = 0
         self.frame = (self.frame + 1) % 4
         self.actor.image = f"{prefix}_{self.state}{self.frame + 1}"

    def update(self):
        if self.dead: return
        self.apply_gravity()
        self.check_platform_collisions()

class Hero(CharacterBase): # ! HERDA DA BASE
    def __init__(self, pos):
        super().__init__("hero_idle1", pos, gravity=0.5, speed=3)

    def handle_input(self):
        move = 0
        if keyboard.left:
            self.actor.x -= self.speed
            self.direction = -1
            move = 1
        elif keyboard.right:
            self.actor.x += self.speed
            self.direction = 1
            move = 1
        if self.on_ground and keyboard.up:
            self.vel_y = -10
        self.actor.flip_x = self.direction < 0
        self.state = "walk" if move else "idle"

    def update(self):
        if self.dead: return
        self.handle_input()
        super().update()
        self.animate("hero")

class Enemy(CharacterBase): # ! HERDA DA BASE
    def __init__(self, pos, left_limit, right_limit):
        super().__init__("enemy_walk1", pos, gravity=0.5, speed=2)
        self.left_limit = left_limit
        self.right_limit = right_limit

    def update(self):
        if self.dead: return
        self.actor.x += self.direction * self.speed
        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.direction *= -1
            self.actor.flip_x = self.direction < 0
        self.state = "walk"
        super().update()
        self.animate("enemy")

hero = Hero((100, 100))
enemies = [
    Enemy((300, 200), 260, 340),
    Enemy((500, 150), 460, 560)
]

for i in range(10):
    a = Actor("block1")
    a.x, a.y = 100 + i * TILE_SIZE, 300
    platforms.append(a)

def update():
    hero.update()
    for e in enemies:
        e.update()


def load_map(path): # ! MAPA
    try:
        with open(path) as f:
            for y, line in enumerate(f.read().strip().split("\n")):
                for x, val in enumerate(line.split(",")):
                    if val in ["21", "22", "23"]:
                        img = "block1"
                    elif val in ["153", "154", "155", "156"]:
                        img = "cloud"
                    else:
                        continue
                    a = Actor(img)
                    a.x, a.y = x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2
                    platforms.append(a)
    except Exception as e:
        print("Erro ao carregar mapa:", e)

def load_obstacles(path):
    for y, line in enumerate(open(path).read().strip().split("\n")):
        for x, val in enumerate(line.split(",")):
            if val != "-1":
                a = Actor("obstacle")
                a.x, a.y = x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2
                obstacles.append(a)

load_map('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')
