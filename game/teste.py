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
