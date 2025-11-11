import pgzrun; from pygame import Rect


TILE_SIZE, ROWS, COLS = 18, 30, 20
WIDTH, HEIGHT = TILE_SIZE * ROWS, TILE_SIZE * COLS
TITLE, BORDER_THICKNESS = "Cloud Parkour", 3

game_state, music_on, sound_on, key_cd = "menu", True, True, 0
platforms, obstacles = [], []
BORDER_COLOR = (180, 200, 255)
borders = {
    "top": Rect(0, 0, WIDTH, BORDER_THICKNESS),
    "bottom": Rect(0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS),
    "left": Rect(0, 0, BORDER_THICKNESS, HEIGHT),
    "right": Rect(WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT),
}

class Character: # ! BASE
    def __init__(self, img, pos, g=0.5, sp=2):
        self.actor, self.vel_y, self.g, self.sp = Actor(img, pos), 0, g, sp
        self.frame, self.anim_t, self.state = 0, 0, "idle"
        self.on_ground, self.dead, self.dir = False, False, 1

    def rect(self):
        return Rect(self.actor.x - 8, self.actor.y - 16, 16, 32)

    def gravity(self):
        self.vel_y += self.g
        self.actor.y += self.vel_y

    def check_platforms(self):
        self.on_ground = False
        hr = self.rect()
        for b in platforms:
            br = Rect(b.x - 9, b.y - 9, 18, 18)
            if hr.colliderect(br) and self.vel_y > 0 and self.actor.y < b.y:
                self.actor.y, self.vel_y, self.on_ground = b.y - 18, 0, True

    def animate(self, prefix):
         self.anim_t += 1
         if self.anim_t > 8:
            self.anim_t, self.frame = 0, (self.frame + 1)
            self.actor.y += (-1) ** self.frame * 1.5
         img_name = f"{prefix}_{self.state}{(self.frame % 4) + 1}"

         try:
            self.actor.image = img_name
         except:
             pass

    def update(self):
        if not self.dead:
            self.gravity()
            self.check_platforms()


class Hero(Character): # ! HEROI (HERDA DA BASE)
    def __init__(self, pos):
        super().__init__("hero_idle1", pos, 0.5, 3)

    def handle_input(self):
        move = 0
        if keyboard.left:
            self.actor.x -= self.sp; self.dir, move = -1, 1
        elif keyboard.right:
            self.actor.x += self.sp; self.dir, move = 1, 1
        if self.on_ground and keyboard.up:
            self.vel_y = -10
        self.actor.flip_x = self.dir < 0
        self.state = "walk" if move else "idle"

    def update(self):
        if not self.dead:
            self.handle_input()
            super().update()
            self.animate("hero")

class Enemy(Character): # ! INIMIGO (HERDA DA BASE)
    def __init__(self, pos, l, r):
        super().__init__("enemy_walk1", pos, 0, 2)
        self.l, self.r = l, r

    def patrol(self):
        self.actor.x += self.dir * self.sp
        if self.actor.x <= self.l or self.actor.x >= self.r:
            self.dir *= -1
            self.actor.flip_x = self.dir < 0

    def update(self):
        if not self.dead:
            self.patrol()
            self.state = "walk"
            self.animate("enemy")

hero = Hero((100, 100))
enemies = [Enemy((300, 150), 260, 340), Enemy((500, 120), 460, 560)]

def load_csv(path, func):
    for y, line in enumerate(open(path).read().strip().split("\n")):
        for x, v in enumerate(line.split(",")): func(x, y, v)

def load_map(p):
    def f(x, y, v):
        img = ("block1" if v in ["21", "22", "23"]
               else "cloud" if v in ["153", "154", "155", "156"]
               else None)
        if img: platforms.append(Actor(img, (x * TILE_SIZE + 9, y * TILE_SIZE + 9)))
    load_csv(p, f)


def load_obstacles(p):
    def f(x, y, v):
        if v != "-1":
            obstacles.append(Actor("obstacle", (x * TILE_SIZE + 9, y * TILE_SIZE + 9)))
    load_csv(p, f)

load_map('C:/Users/PC/Documents/GitHub/roguelike/game/plataformer.csv')
load_obstacles('C:/Users/PC/Documents/GitHub/roguelike/game/obstacles.csv')


def toggle_music():
    global music_on
    music_on = not music_on
    (music.play if music_on else music.stop)('bg_music')


def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on: sounds.menu_click.play()


def start_game():
    global game_state
    if sound_on: sounds.menu_click.play()
    game_state = "playing"


def draw_menu():
    screen.clear()
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, 80), fontsize=50, color="white")
    opts = [f"{i+1} - {t}" for i, t in enumerate([
        "Start Game",
        f"Music: {'ON' if music_on else 'OFF'}",
        f"Sounds: {'ON' if sound_on else 'OFF'}",
        "Exit"
    ])]
    for i, t in enumerate(opts):
        screen.draw.text(t, center=(WIDTH // 2, 180 + i * 70), fontsize=40)


def update_menu():
    global key_cd
    if key_cd > 0: key_cd -= 1; return
    if keyboard.K_1: start_game()
    elif keyboard.K_2: toggle_music(); key_cd = 10
    elif keyboard.K_3: toggle_sound(); key_cd = 10
    elif keyboard.K_4: exit()
    if music_on and not music.is_playing('bg_music'):
        music.play('bg_music')


def handle_border_collision():
    global game_state
    if hero.actor.x < BORDER_THICKNESS + 8:
        hero.actor.x = BORDER_THICKNESS + 8
    elif hero.actor.x > WIDTH - BORDER_THICKNESS - 8:
        hero.actor.x = WIDTH - BORDER_THICKNESS - 8
    if hero.actor.y < BORDER_THICKNESS + 16:
        hero.actor.y = BORDER_THICKNESS + 16
    elif hero.actor.y > HEIGHT - BORDER_THICKNESS - 16:
        hero.dead, game_state = True, "dead"


def check_collisions():
    r = hero.rect()
    if any(r.colliderect(e.rect()) for e in enemies) or any(
        r.colliderect(Rect(o.x - 8, o.y - 8, 16, 16)) for o in obstacles):
        hero.dead, globals()["game_state"] = True, "dead"


def update_menu():
    global key_cd
    if key_cd > 0: key_cd -= 1; return
    if keyboard.K_1: start_game()
    elif keyboard.K_2: toggle_music(); key_cd = 10
    elif keyboard.K_3: toggle_sound(); key_cd = 10
    elif keyboard.K_4: exit()
    
    if music_on and not music.is_playing('bg_music'):
        music.play('bg_music')

def draw():
    screen.fill((60, 100, 160))
    [screen.draw.filled_rect(b, BORDER_COLOR) for b in borders.values()]
    if game_state == "menu": draw_menu(); return
    [a.draw() for a in platforms + obstacles]
    [e.actor.draw() for e in enemies]
    hero.actor.draw()
    if game_state == "dead":
        screen.draw.text("YOU DIED!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=60, color="red", shadow=(2, 2))

pgzrun.go()