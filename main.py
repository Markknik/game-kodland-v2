import pgzrun
import random
import pygame
from pygame import mixer

mixer.init()

WIDTH = 1200
HEIGHT = 600
TITLE = "Simple Platformer"

# Game states
GAME_STATE = "menu"

jump_sound = mixer.Sound('jump.wav')

background_music = mixer.Channel(0)
background_music.play(pygame.mixer.Sound('chilly.wav'), loops=-1)


class AnimatedSprite:
    def __init__(self, images, pos):
        self.images = images
        self.pos = pos
        self.current_frame = 0
        self.frame_count = len(images)
        self.image = images[0]

    def update(self):
        self.current_frame = (self.current_frame + 1) % self.frame_count
        self.image = self.images[self.current_frame]

    def draw(self):
        self.image.pos = self.pos
        self.image.draw()


class Player(AnimatedSprite):
    def __init__(self, images, pos):
        super().__init__(images, pos)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.health = 100

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        global GAME_STATE
        self.health = 0
        GAME_STATE = "dead"  # Переходим в состояние "мертвый"
        background_music.stop()  # Останавливаем музыку
        jump_sound.stop()  # Останавливаем звуки

    def update(self):
        super().update()
        if keyboard.left:
            self.vx = -2
        elif keyboard.right:
            self.vx = 2
        else:
            self.vx = 0

        if keyboard.up:
            self.vy = -10
            self.on_ground = False
            jump_sound.play()

        self.vy += 0.5

        self.pos[0] += self.vx
        self.pos[1] += self.vy

        if self.pos[1] > HEIGHT - 50:
            self.pos[1] = HEIGHT - 50
            self.on_ground = True
            self.vy = 0

        self.on_ground = False
        for block in blocks:
            if self.collides_with(block):
                if self.vy > 0 and self.pos[1] + self.image.height <= block.pos[1] + self.vy:
                    self.pos[1] = block.pos[1] - self.image.height
                    self.on_ground = True
                    self.vy = 0

    def collides_with(self, other):
        return (self.pos[0] + self.image.width > other.pos[0] and self.pos[0] < other.pos[0] + other.image.width) and \
            (self.pos[1] + self.image.height > other.pos[1] and self.pos[1] < other.pos[1] + other.image.height)


class Enemy(AnimatedSprite):
    def __init__(self, images, pos):
        super().__init__(images, pos)
        self.direction = random.choice([-1, 1])
        self.vx = 1 * self.direction

    def collides_with(self, other):
        return (self.pos[0] + self.image.width > other.pos[0] >= self.pos[0] or
                other.pos[0] + other.image.width > self.pos[0] >= other.pos[0]) and \
            (self.pos[1] + self.image.height > other.pos[1] >= self.pos[1] or
             other.pos[1] + other.image.height > self.pos[1] >= other.pos[1])

    def update(self):
        super().update()
        self.pos[0] += self.vx
        if self.pos[0] < 0 or self.pos[0] > WIDTH - self.image.width:
            self.direction *= -1
            self.vx *= -1

        if self.collides_with(player):
            player.take_damage(5)


class Block:
    def __init__(self, image, pos):
        self.image = Actor(image)
        self.image.pos = pos
        self.pos = pos

    def draw(self):
        self.image.draw()


# Load images
player_images = [Actor("player_frame_1")]
enemy_image1 = [Actor("enemy_frame_1")]
enemy_image2 = [Actor("enemy_frame_2")]
enemy_image3 = [Actor("enemy_frame_3")]
enemy_image0 = [Actor("enemy_frame_0")]
block_image = "block"

# Initialize player and enemies
player = Player(player_images, [WIDTH // 2, HEIGHT - 50])
enemies = [Enemy(enemy_image1, [random.randint(0, WIDTH), HEIGHT - 50]),
           Enemy(enemy_image2, [random.randint(0, WIDTH), HEIGHT - 50]),
           Enemy(enemy_image3, [random.randint(0, WIDTH), HEIGHT - 50]),
           Enemy(enemy_image0, [random.randint(0, WIDTH), HEIGHT - 50])]
blocks = [Block("block", (100, 400)),
          Block("block", (400, 500)),
          Block("block", (300, 400)),
          Block("block", (800, 200)),
          Block("block", (650, 400)),
          Block("block", (1000, 200)),
          Block("block", (600, 300))]


def draw():
    if GAME_STATE == "menu":
        screen.clear()
        screen.draw.text("Simple Platformer", center=(WIDTH // 2, HEIGHT // 3), fontsize=60)
        screen.draw.text("Press SPACE to Start", center=(WIDTH // 2, HEIGHT // 2), fontsize=40)
        screen.draw.text("Press ESC to Exit", center=(WIDTH // 2, HEIGHT // 1.5), fontsize=40)
    elif GAME_STATE == "playing":
        screen.clear()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for block in blocks:
            block.draw()
        screen.draw.text(f"Health: {player.health}", (10, 10), fontsize=40, color="white")
    elif GAME_STATE == "dead":
        screen.draw.text("You Died!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60)
        screen.draw.text("Press SPACE to Restart", center=(WIDTH // 2, HEIGHT // 1.5), fontsize=40)
        screen.draw.text("Press ESC to Quit", center=(WIDTH // 2, HEIGHT // 1.75), fontsize=40)


def update():
    global GAME_STATE
    if GAME_STATE == "menu":
        if keyboard.space:
            GAME_STATE = "playing"
    elif GAME_STATE == "playing":
        player.update()
        for enemy in enemies:
            enemy.update()
    elif GAME_STATE == "dead":
        if keyboard.space:
            restart_game()
        elif keyboard.escape:
            exit()


def restart_game():
    global GAME_STATE, player, enemies
    GAME_STATE = "playing"
    player = Player(player_images, [WIDTH // 2, HEIGHT - 50])
    enemies = [Enemy(enemy_image1, [random.randint(0, WIDTH), HEIGHT - 50]),
               Enemy(enemy_image2, [random.randint(0, WIDTH), HEIGHT - 50]),
               Enemy(enemy_image3, [random.randint(0, WIDTH), HEIGHT - 50]),
               Enemy(enemy_image0, [random.randint(0, WIDTH), HEIGHT - 50])]
    background_music.play(pygame.mixer.Sound('chilly.wav'), loops=-1)


pgzrun.go()
