from ursina import *
from random import uniform, choice
import os, sys

app = Ursina()

# Player setup
player = Entity(model='cube', color=color.azure, scale=(1,1,1), collider='box', position=(0,0,0))

# Ground
ground = Entity(model='plane', texture='white_cube', texture_scale=(20,20),
                scale=(40,1,40), color=color.lime, collider='box')

camera.position = (0, 20, -30)
camera.rotation_x = 30

# UI Elements
score = 0
level = 1
final_level = 3  # Total levels
coins_to_collect = 5

score_text = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=2, origin=(0,0), background=True)
level_text = Text(text=f'Level: {level}', position=(-0.85, 0.38), scale=2, origin=(0,0), background=True)
Text(text='WASD to move. Collect coins. Avoid enemies!', position=(-0.6, 0.4), scale=1.5, origin=(0,0))

# Coin setup
coins = []
def spawn_coins(n):
    coins.clear()
    for _ in range(n):
        x = uniform(-18, 18)
        z = uniform(-18, 18)
        coin = Entity(model='sphere', color=color.yellow, scale=0.5, position=(x,0.5,z), collider='sphere')
        coins.append(coin)
spawn_coins(coins_to_collect)

# Enemy setup
enemies = []
def spawn_enemies(n):
    for enemy in enemies:
        destroy(enemy)
    enemies.clear()
    for _ in range(n):
        x = uniform(-15, 15)
        z = uniform(-15, 15)
        enemy = Entity(model='cube', color=color.red, scale=1, position=(x,0.5,z), collider='box')
        enemies.append(enemy)
spawn_enemies(level)

# Movement speed
speed = 5

# Restart game on game over
def restart_game():
    application.quit()
    os.execl(sys.executable, sys.executable, *sys.argv)

# Advance to next level or end
def next_level():
    global level, coins_to_collect
    if level < final_level:
        level += 1
        coins_to_collect += 3
        level_text.text = f'Level: {level}'
        spawn_coins(coins_to_collect)
        spawn_enemies(level)
        player.position = (0, 0, 0)
    else:
        application.pause()
        Text(text='🎉 You Win! 🎉', origin=(0,0), scale=3, background=True, color=color.green)

def update():
    global score

    # Player movement
    if held_keys['w']:
        player.z += time.dt * speed
    if held_keys['s']:
        player.z -= time.dt * speed
    if held_keys['a']:
        player.x -= time.dt * speed
    if held_keys['d']:
        player.x += time.dt * speed

    # Coin collection
    for coin in coins[:]:
        if player.intersects(coin).hit:
            destroy(coin)
            coins.remove(coin)
            score += 1
            score_text.text = f'Score: {score}'

    # If all coins collected
    if not coins:
        Text(text='Level Complete!', origin=(0,0), scale=2, background=True, color=color.orange)
        invoke(next_level, delay=2)

    # Enemy collision
    for enemy in enemies:
        enemy.x += choice([-1, 1]) * time.dt * 2
        enemy.z += choice([-1, 1]) * time.dt * 2
        if player.intersects(enemy).hit:
            application.pause()
            Text(text='Game Over! Hit by Enemy.', origin=(0,0), scale=2, background=True)
            invoke(restart_game, delay=3)
            return

app.run()