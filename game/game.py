import math # ? serve pra calculos de posição, colisão e movimento

import pgzrun

WIDTH = 800
HEIGHT = 600
TITLE = "BOSTAAAAAAAAAAA"

<<<<<<< HEAD
def update():
    pass

def draw():
    screen.fill((0, 126, 0))
    pass

pgzrun.go()
    
# * update() atualizar o jogo toda hora 
=======
# Cria o personagem principal (hero) com a imagem no assets
hero = Actor("hero_idle", (400, 300))

def draw():
    screen.clear()
    hero.draw()

# Atualiza o jogo (movimento, lógica, etc)
def update():
    if keyboard.left:
        hero.x -= 5
    if keyboard.right:
        hero.x += 5
    if keyboard.up:
        hero.y -= 5
    if keyboard.down:
        hero.y += 5

pgzrun.go()



# * update() atualizar o jogo toda hora
>>>>>>> 360f9978df28702ca55c3d3680d9ec03125884e3
# draw() desenha o jogo 
# actor() objeto/coisa com imagem que pode aparecer na tela 
# * WIDTH e HEIGHT é pra definição do tamanho da tela
# screen.draw() é pra apresentar na tela
# Actor.pos ou Actor.x / Actor.y → define posição na tela
# Actor.draw() → desenha o sprite na tela atual

# ! • EXEMPLO DE DETECÇÃO DE MOVIMENTO

# if keyboard.left:
#   hero.x -= 5  # move 5 pixels para esquerda
# if keyboard.right:
#    hero.x += 5  # move 5 pixels para direita

# ! • EXEMPLO DE DETECÇÃO DE GRAVIDADE . \path\to\venv\Scripts\Activate.

# hero.vy += 0.5  # aceleração da gravidade
# hero.y += hero.vy

# if hero.y >= GROUND_Y:  # chão
  #  hero.y = GROUND_Y
  #  hero.vy = 0

# ! • EXEMPLO DE DETECÇÃO DE RELAÇÃO IMAGEM/ACTOR

# hero = Actor('hero_idle')
# hero.image = 'hero_run1'

# ! • EXEMPLO DE DETECÇÃO DE ANIMAÇÃO SPRITE

# frames = ['hero_run1', 'hero_run2', 'hero_run3']
# hero.frame = (hero.frame + 0.1) % len(frames)
# hero.image = frames[int(hero.frame)]



# Actor.pos ou Actor.x / Actor.y → define posição na tela
# Actor.draw() → desenha o sprite na tela atual