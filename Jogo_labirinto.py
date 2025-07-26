import random
from math import floor
from pygame import Rect
import pgzrun

WIDTH = 800
HEIGHT = 600
TITLE = "Dungeon Escape - Roguelike"

TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

hero_idle = ["adventurer-idle-01.png", "adventurer-idle-02.png"]
hero_walk = ["adventurer-run-00.png", "adventurer-run-01.png", "adventurer-run-02.png", "adventurer-run-03.png", "adventurer-run-04.png", "adventurer-run-05.png"]
enemy_idle = ["walk01.png", "walk02.png", "walk03.png", "walk04.png", "walk05.png", "walk06.png", "walk07.png", "walk08.png"]

map_data = [[random.choice([0, 0, 0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
map_data[1][1] = 0
map_data[GRID_HEIGHT - 2][GRID_WIDTH - 2] = 2

game_state = "menu"
sounds_on = True
music_playing = False

def toggle_music():
    global music_playing
    if sounds_on:
        if not music_playing:
            music.play("bgm")
            music.set_volume(0.5)
            music_playing = True
    else:
        music.stop()
        music_playing = False

class Player:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.sprite_index = 0
        self.frame_count = 0
        self.image = hero_idle[0]
        self.moving = False
        self.direction = (0, 0)

    def update(self):
        if self.moving:
            self.x += self.direction[0] * 4
            self.y += self.direction[1] * 4
            if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
                self.grid_x += self.direction[0]
                self.grid_y += self.direction[1]
                self.direction = (0, 0)
                self.moving = False
        self.animate()

    def move(self, dx, dy):
        if self.moving: return
        nx, ny = self.grid_x + dx, self.grid_y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and map_data[ny][nx] != 1:
            self.direction = (dx, dy)
            self.moving = True

    def animate(self):
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.sprite_index = (self.sprite_index + 1) % len(hero_idle)
            self.image = hero_walk[self.sprite_index] if self.moving else hero_idle[self.sprite_index]

    def draw(self):
        screen.blit(self.image, (self.x, self.y)) # type: ignore

class Enemy:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.sprite_index = 0
        self.frame_count = 0
        self.image = enemy_idle[0]
        self.direction = (0, 0)
        self.moving = False
        self.move_timer = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count % 20 == 0:
            self.sprite_index = (self.sprite_index + 1) % len(enemy_idle)
            self.image = enemy_idle[self.sprite_index]

        if self.moving:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2
            if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
                self.grid_x += self.direction[0]
                self.grid_y += self.direction[1]
                self.direction = (0, 0)
                self.moving = False
        else:
            self.move_timer += 1
            if self.move_timer >= 60:
                self.move_timer = 0
                self.try_move()

    def try_move(self):
        dx, dy = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        nx, ny = self.grid_x + dx, self.grid_y + dy
        if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and
            abs(nx - self.start_x) <= 2 and abs(ny - self.start_y) <= 2 and
            map_data[ny][nx] != 1):
            self.direction = (dx, dy)
            self.moving = True

    def draw(self):
        screen.blit(self.image, (self.x, self.y)) # type: ignore

player = Player(1, 1)
enemies = [Enemy(random.randint(3, GRID_WIDTH - 2), random.randint(3, GRID_HEIGHT - 2)) for _ in range(3)]

menu_buttons = [
    Rect(300, 200, 200, 50),
    Rect(300, 270, 200, 50),
    Rect(300, 340, 200, 50),
]

def draw_menu():
    screen.fill("black") # type: ignore
    screen.draw.text("Dungeon Escape", center=(WIDTH//2, 100), fontsize=50, color="white") # type: ignore
    screen.draw.filled_rect(menu_buttons[0], "darkgreen") # type: ignore
    screen.draw.text("Start Game", center=menu_buttons[0].center, color="white") # type: ignore
    screen.draw.filled_rect(menu_buttons[1], "darkblue") # type: ignore
    screen.draw.text("Sound ON" if sounds_on else "Sound OFF", center=menu_buttons[1].center, color="white") # type: ignore
    screen.draw.filled_rect(menu_buttons[2], "darkred") # type: ignore
    screen.draw.text("Exit", center=menu_buttons[2].center, color="white") # type: ignore

def on_mouse_down(pos):
    global game_state, sounds_on
    if game_state == "menu":
        if menu_buttons[0].collidepoint(pos):
            game_state = "playing"
            if sounds_on and not music_playing:
                toggle_music()
        elif menu_buttons[1].collidepoint(pos):
            sounds_on = not sounds_on
            toggle_music()
        elif menu_buttons[2].collidepoint(pos):
            exit()

def update():
    if game_state == "playing":
        if music_playing and not music.is_playing("bgm"):
            usic.play("bgm")
        player.update()
        for enemy in enemies:
            enemy.update()
        for enemy in enemies:
            if player.grid_x == enemy.grid_x and player.grid_y == enemy.grid_y:
                # sounds.play("hit") 
                print("Game Over!")
                exit()
        if map_data[player.grid_y][player.grid_x] == 2:
            print("You Win!")
            # sounds.play("win") 
            exit()

def draw():
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        screen.fill("black") # type: ignore
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile = map_data[y][x]
                color = "gray" if tile == 1 else "gold" if tile == 2 else "darkgray"
                screen.draw.filled_rect(Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), color) # type: ignore
        player.draw()
        for enemy in enemies:
            enemy.draw()

def on_key_down(key):
    if game_state == "playing":
        if key == keys.UP: player.move(0, -1) # type: ignore
        elif key == keys.DOWN: player.move(0, 1) # type: ignore
        elif key == keys.LEFT: player.move(-1, 0) # type: ignore
        elif key == keys.RIGHT: player.move(1, 0) # type: ignore
