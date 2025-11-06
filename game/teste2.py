import pgzrun
from pygame import Rect

TILE_SIZE, ROWS, COLS = 18, 30, 20
WIDTH, HEIGHT = TILE_SIZE * ROWS, TILE_SIZE * COLS
TITLE = "Platformer Adventure"

game_state, music_on, sound_on, key_cooldown = "menu", True, True, 0
platforms, obstacles, enemies = [], [], []


class Hero:
    def __init__(self, x, y):
        self.actor = Actor("hero_idle1", (x, y))
        self.vel_y, self.gravity = 0, 0.5
        self.dead, self.on_ground = False, False
        self.frame, self.anim_timer, self.state = 0, 0, "idle"

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
        self.actor.flip_x = move < 0
        self.state = "walk" if move else "idle"

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

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % 4
            self.actor.image = f"hero_{self.state}{self.frame + 1}"


hero = Hero(100, 100)


class Enemy:
    def __init__(self, x, y, left, right):
        self.actor = Actor("enemy_walk1", (x, y))
        self.left_limit, self.right_limit = left, right
        self.direction, self.frame, self.anim_timer = 1, 0, 0

    def rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 8, 16, 16)

    def update(self):
        self.actor.x += self.direction * 2
        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.direction *= -1
            self.actor.flip_x = self.direction < 0
        self.animate()

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.frame += 1
            fnum = (self.frame % 3) + 1
            self.actor.image = f"enemy_walk{fnum}"


enemies.extend([Enemy(300, 200, 260, 340), Enemy(500, 150, 460, 560)])


def load_map(path):
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


load_map("C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv")
load_obstacles("C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv")


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


def draw_menu():
    screen.clear()
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, 80), fontsize=50, color="white")
    for i, txt in enumerate([
        "1 - Start Game",
        f"2 - Music: {'ON' if music_on else 'OFF'}",
        f"3 - Sounds: {'ON' if sound_on else 'OFF'}",
        "4 - Exit"
    ]):
        screen.draw.text(txt, center=(WIDTH // 2, 180 + i * 70), fontsize=40)


def update_menu():
    global game_state, key_cooldown
    if key_cooldown > 0:
        key_cooldown -= 1
        return
    if keyboard.K_1:
        start_game()
    elif keyboard.K_2:
        toggle_music()
        if sound_on: sounds.menu_click.play()
        key_cooldown = 10
    elif keyboard.K_3:
        toggle_sound()
        key_cooldown = 10
    elif keyboard.K_4:
        exit()


def start_game():
    global game_state
    if sound_on: sounds.menu_click.play()
    game_state = "playing"


def update():
    if game_state == "menu":
        update_menu()
        return
    if hero.dead:  # pausa o jogo se morto
        return
    hero.update()
    for e in enemies:
        e.update()
    check_collisions()


def check_collisions():
    global game_state
    r = hero.rect()
    for e in enemies:
        if r.colliderect(e.rect()):
            hero.dead = True
            game_state = "dead"
            if sound_on: sounds.hit.play()
    for o in obstacles:
        if r.colliderect(Rect(o.x - 8, o.y - 8, 16, 16)):
            hero.dead = True
            game_state = "dead"
            if sound_on: sounds.hit.play()


def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
        return
    for b in platforms: b.draw()
    for o in obstacles: o.draw()
    for e in enemies: e.actor.draw()
    hero.actor.draw()
    if hero.dead:
        screen.draw.text(
            "YOU DIED!",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=60,
            color="red",
            shadow=(2, 2)
        )


start_music()
pgzrun.go()
