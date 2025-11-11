import pgzrun; from pygame import Rect

TILE_SIZE, ROWS, COLS = 18, 30, 20 
WIDTH, HEIGHT = TILE_SIZE * ROWS, TILE_SIZE * COLS
TITLE = "Cloud Parkour" 

game_state, music_on, sound_on, key_cooldown = "menu", True, True, 0
platforms, obstacles  = [], []

class Character: # ! PRINCIPAL
    def __init__(self, x, y):
        self.actor = Actor(x, y)
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


        
