import os
import sys
import time
import subprocess
import pip
from os import environ
import math
import textwrap
import json
import random

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
restart = False
display = 0
slow_motion = False
slow_factor = 0.3
slow_duration = 2000
slow_start = 0
kill_streak = 0
last_kill = 0
combo_text = ""
combo_alpha = 0
steak_sound = False
god_status = False
inf_money = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
DIALOGUE_BG = (30, 30, 40)
DIALOGUE_BORDER = (70, 70, 90)

def import_lib(name):
    global restart
    try:
        return __import__(name)
    except ImportError:
        restart = True
        subprocess.check_call([sys.executable, "-m", "pip", "install", name])
    return __import__(name)


def check_file(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True


print("[ZOMBIE PROJECT] Проверка библиотек...")
import_lib("tqdm")
import tqdm

for i in tqdm.tqdm(["colorama", "pygame"]):
    import_lib(i)

if restart:
    while True:
        input("[ZOMBIE PROJECT] Установлены библиотеки. Перезапустите скрипт и нажмите Enter...")

import colorama
from colorama import Fore, Style
import pygame

colorama.init()


def start_menu():
    global display, steak_sound, god_status, inf_money
    try:
        print(f"\n{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Fore.LIGHTWHITE_EX} ГЛАВНОЕ МЕНЮ ---")
        print(f"{Fore.LIGHTGREEN_EX}[CREDITS]{Style.RESET_ALL} Андрей Сайгин П-63")
        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 1 - Запустить игру")
        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 2 - Настройки")
        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 3 - Выйти")
        choice = int(input(f"\n{Fore.LIGHTGREEN_EX}[>]{Style.RESET_ALL} Выбор: "))
        if choice == 1:
            return
        elif choice == 2:
            print(f"\n{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Style.RESET_ALL} НАСТРОЙКИ ---")
            print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 1 - Дисплей")
            print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 2 - Фан (может испортить впечетления)")
            print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 3 - Назад")
            choice = int(input(f"{Fore.LIGHTGREEN_EX}[>]{Style.RESET_ALL} Выбор: "))
            if choice == 1:
                display = int(input(f"{Fore.LIGHTGREEN_EX}[>]{Style.RESET_ALL} Номер дисплея (1 = основной): ")) - 1
            elif choice == 2:
                while True:
                    print(f"\n{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Style.RESET_ALL} НАСТРОЙКИ ---")
                    if steak_sound:
                        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 1 - Звуки при комбо {Fore.GREEN}[ВКЛ]")
                    else:
                        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 1 - Звуки при комбо {Fore.RED}[ВЫКЛ]")
                    if god_status:
                        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 2 - Режим Бога {Fore.GREEN}[ВКЛ]")
                    else:
                        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 2 - Режим Бога {Fore.RED}[ВЫКЛ]")
                    if inf_money:
                        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 3 - Бесконечные деньги {Fore.GREEN}[ВКЛ]")
                    else:
                        print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 3 - Бесконечные деньги {Fore.RED}[ВЫКЛ]")
                    print(f"{Fore.LIGHTGREEN_EX}[-]{Style.RESET_ALL} 4 - Старт")
                    choice = int(input(f"{Fore.LIGHTGREEN_EX}[>]{Style.RESET_ALL} Выбор: "))
                    if choice == 1:
                        if steak_sound:
                            steak_sound = False
                        else:
                            steak_sound = True
                    elif choice == 2:
                        if god_status:
                            god_status = False
                        else:
                            god_status = True
                    elif choice == 3:
                        if inf_money:
                            inf_money = False
                        else:
                            inf_money = True
                    else:
                        return
            else:
                start_menu()
        elif choice == 3:
            sys.exit()
    except:
        print("[!] Ошибка, возврат в меню...")
        time.sleep(1)
        return start_menu()


start_menu()
print(f"{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Style.RESET_ALL} {Fore.GREEN}Инициализация PYGAME...{Style.RESET_ALL}")
pygame.init()
pygame.mixer.init()

print(f"{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Style.RESET_ALL} {Fore.GREEN}Загрузка...{Style.RESET_ALL}")

WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[display]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DIALOGUE_BG = (30, 30, 40)
DIALOGUE_BORDER = (70, 70, 90)


def draw_text(surface, text, font, color, x, y, max_width):
    lines = textwrap.wrap(text, width=max_width // font.size(' ')[0])
    for i, line in enumerate(lines):
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y + i * font.get_height()))


def draw_hud(screen, player):
    pygame.draw.rect(screen, RED, (20, 20, 200, 20))
    pygame.draw.rect(screen, GREEN, (20, 20, 200 * (player.health / player.max_health), 20))

    font = pygame.font.SysFont("Benzin", 36)
    text = font.render(f"HP: {player.health}", True, WHITE)
    screen.blit(text, (230, 15))

    text = font.render(f"Money: ${player.money}", True, YELLOW)
    screen.blit(text, (20, 50))

    if player.current_weapon:
        text = font.render(f"{player.current_weapon.name} ({player.current_weapon.ammo})", True, WHITE)
        screen.blit(text, (20, 85))

    slot_size = 40
    padding = 10
    start_x = WIDTH - (3 * (slot_size + padding)) - 20

    for i in range(3):
        slot_rect = pygame.Rect(start_x + i * (slot_size + padding), HEIGHT - slot_size - 20, slot_size, slot_size)
        pygame.draw.rect(screen, GRAY, slot_rect, 2)

        if i < len(player.weapons):
            weapon = player.weapons[i]
            pygame.draw.rect(screen, weapon.color, slot_rect.inflate(-10, -10))

            if weapon == player.current_weapon:
                pygame.draw.rect(screen, GREEN, slot_rect, 3)

            num_text = font.render(str(i + 1), True, WHITE)
            screen.blit(num_text, (slot_rect.x + 5, slot_rect.y + 5))


class Background:
    def __init__(self, image_path, speed_factor=0.5, scale=2.0):
        self.original_image = pygame.image.load(image_path).convert()
        self.scale = scale
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * self.scale),
             int(self.original_image.get_height() * self.scale)
             )
        )
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed_factor = speed_factor
        self.x = 0
        self.y = 0

    def update(self, player_x, player_y):
        self.x = -player_x * self.speed_factor % self.width
        self.y = -player_y * self.speed_factor % self.height

    def draw(self, screen, camera_x, camera_y):
        screen_width, screen_height = screen.get_size()

        screen.blit(self.image, (self.x - camera_x * self.speed_factor,
                                 self.y - camera_y * self.speed_factor))

        if self.x - camera_x * self.speed_factor > 0:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor - self.width,
                                     self.y - camera_y * self.speed_factor))
        else:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor + self.width,
                                     self.y - camera_y * self.speed_factor))

        if self.y - camera_y * self.speed_factor > 0:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor,
                                     self.y - camera_y * self.speed_factor - self.height))
        else:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor,
                                     self.y - camera_y * self.speed_factor + self.height))

        if self.x - camera_x * self.speed_factor > 0 and self.y - camera_y * self.speed_factor > 0:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor - self.width,
                                     self.y - camera_y * self.speed_factor - self.height))
        elif self.x - camera_x * self.speed_factor > 0:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor - self.width,
                                     self.y - camera_y * self.speed_factor + self.height))
        elif self.y - camera_y * self.speed_factor > 0:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor + self.width,
                                     self.y - camera_y * self.speed_factor - self.height))
        else:
            screen.blit(self.image, (self.x - camera_x * self.speed_factor + self.width,
                                     self.y - camera_y * self.speed_factor + self.height))

background = Background("ZOMBIE-PROJECT/background.png", speed_factor=0.3, scale=1.5)

class Weapon:
    def __init__(self, name, damage, fire_rate, ammo, color, bullet_speed=10, spread=0, auto=False, price=0):
        self.name = name
        self.damage = damage
        self.fire_rate = fire_rate
        self.max_ammo = ammo
        self.ammo = ammo
        self.color = color
        self.bullet_speed = bullet_speed
        self.spread = spread
        self.auto = auto
        self.last_shot = 0
        self.price = price

    def can_shoot(self, current_time):
        return current_time - self.last_shot > 1000 / self.fire_rate

    def shoot(self, x, y, target_x, target_y, current_time):
        if self.ammo <= 0 or not self.can_shoot(current_time):
            return []

        self.ammo -= 1
        self.last_shot = current_time

        bullets = []
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        dx, dy = dx / dist, dy / dist

        if self.spread > 0:
            angle = math.atan2(dy, dx)
            angle += math.radians((random.random() - 0.5) * self.spread)
            dx, dy = math.cos(angle), math.sin(angle)

        bullets.append(Bullet(x, y, dx, dy, self.bullet_speed, self.damage, self.color))
        return bullets


class Bullet:
    def __init__(self, x, y, dir_x, dir_y, speed, damage, color):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = speed
        self.damage = damage
        self.color = color
        self.angle = math.atan2(dir_y, dir_x)
        self.rect = pygame.Rect(x, y, 10, 5)

    def update(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen, cam_x, cam_y):
        bullet_surf = pygame.Surface((10, 5), pygame.SRCALPHA)
        pygame.draw.rect(bullet_surf, self.color, (0, 0, 10, 5))
        rotated = pygame.transform.rotate(bullet_surf, -math.degrees(self.angle))

        pos = (self.x - cam_x - rotated.get_width() / 2,
               self.y - cam_y - rotated.get_height() / 2)
        screen.blit(rotated, pos)



class Player:
    def __init__(self, x, y, w, h):
        self.standing_image = pygame.image.load(
            os.path.join("ZOMBIE-PROJECT/player", "character_maleAdventurer_side.png")).convert_alpha()
        self.walking_images = [
            pygame.image.load(os.path.join("ZOMBIE-PROJECT/player", f"character_maleAdventurer_run{i}.png")).convert_alpha() for i in
            range(3)]
        self.jump_image = pygame.image.load(os.path.join("ZOMBIE-PROJECT/player", "character_maleAdventurer_jump.png")).convert_alpha()

        self.size_factor = 0.5
        self.standing_image = pygame.transform.scale(self.standing_image, (
        int(self.standing_image.get_width() * self.size_factor),
        int(self.standing_image.get_height() * self.size_factor)))
        self.walking_images = [pygame.transform.scale(img, (
        int(img.get_width() * self.size_factor), int(img.get_height() * self.size_factor))) for img in
                               self.walking_images]
        self.jump_image = pygame.transform.scale(self.jump_image, (
        int(self.jump_image.get_width() * self.size_factor), int(self.jump_image.get_height() * self.size_factor)))

        self.current_image = self.standing_image
        self.rect = self.current_image.get_rect(center=(x, y))

        self.vel_y = 0
        self.speed = 5
        self.gravity = 0.8
        self.jump_power = -15
        self.on_ground = False
        self.max_health = 500
        if god_status:
            self.max_health = 999999
        self.health = self.max_health
        self.money = 10000
        if inf_money:
            self.money = 999999
        self.can_move = True
        self.facing_right = True
        self.old_facing = True

        self.weapons = []
        self.current_weapon = None
        self.weapon_slots = 3
        self.recoil_offset = 0

        self.walk_frame = 0
        self.walk_speed = 5
        self.walk_counter = 0

        pistol = Weapon("Pistol", 1, 2, 30, BLUE)
        self.add_weapon(pistol)

    def add_weapon(self, weapon):
        if len(self.weapons) < self.weapon_slots:
            self.weapons.append(weapon)
            if not self.current_weapon:
                self.current_weapon = weapon
            return True
        return False

    def switch_weapon(self, slot):
        if 0 <= slot < len(self.weapons):
            self.current_weapon = self.weapons[slot]
            return True
        return False

    def move(self, platforms):
        if not self.can_move:
            return

        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_1]:
            self.switch_weapon(0)
        elif keys[pygame.K_2]:
            self.switch_weapon(1)
        elif keys[pygame.K_3]:
            self.switch_weapon(2)

        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]

        if move_left:
            dx = -self.speed
        if move_right:
            dx = self.speed

        if dx != 0:
            self.facing_right = dx > 0

        if dx != 0 and self.on_ground:
            self.walk_counter += 1
            if self.walk_counter >= self.walk_speed:
                self.walk_counter = 0
                self.walk_frame = (self.walk_frame + 1) % len(self.walking_images)
            self.current_image = self.walking_images[self.walk_frame]
        elif self.on_ground:
            self.current_image = self.standing_image

        self.vel_y += self.gravity
        self.vel_y = min(self.vel_y, 20)
        dy += self.vel_y

        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx > 0:
                    self.rect.right = platform.left
                if dx < 0:
                    self.rect.left = platform.right

        self.rect.y += dy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power

        if not self.on_ground:
            self.current_image = self.jump_image

        image_to_draw = self.current_image
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.current_image, True, False)
        self.image_to_draw = image_to_draw

    def draw(self, screen, cam_x, cam_y):
        screen.blit(self.image_to_draw, self.rect.move(-cam_x, -cam_y))

        if self.current_weapon:
            if self.current_weapon.ammo <= 0:
                self.weapons.remove(self.current_weapon)
                self.current_weapon = None
                return

            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_mouse_x = mouse_x + cam_x
            world_mouse_y = mouse_y + cam_y

            dx = world_mouse_x - self.rect.centerx
            dy = world_mouse_y - self.rect.centery
            angle = math.atan2(dy, dx)

            target_direction = 1 if dx > 0 else -1
            if not hasattr(self, 'weapon_direction'):
                self.weapon_direction = target_direction
            if self.weapon_direction != target_direction:
                self.weapon_direction = target_direction
                self.weapon_flip_timer = pygame.time.get_ticks()

            if not hasattr(self, 'weapon_angle_smooth'):
                self.weapon_angle_smooth = angle

            diff = angle - self.weapon_angle_smooth
            if abs(diff) > math.pi:
                diff -= math.copysign(2 * math.pi, diff)
            self.weapon_angle_smooth += diff * 0.2

            if pygame.mouse.get_pressed()[0] and self.current_weapon.can_shoot(pygame.time.get_ticks()):
                self.recoil_offset = -15
            elif self.recoil_offset < 0:
                self.recoil_offset += 1

            weapon_surf = pygame.Surface((40, 20), pygame.SRCALPHA)
            pygame.draw.rect(weapon_surf, self.current_weapon.color, (0, 0, 40, 10))

            rotated = pygame.transform.rotate(weapon_surf, -math.degrees(self.weapon_angle_smooth))

            offset_distance = 20 + self.recoil_offset
            offset = pygame.math.Vector2(offset_distance, 0).rotate(-math.degrees(self.weapon_angle_smooth))
            weapon_pos = pygame.Vector2(self.rect.centerx, self.rect.centery - 10) + offset

            screen.blit(rotated,
                        weapon_pos - pygame.Vector2(rotated.get_width() / 2, rotated.get_height() / 2) - (cam_x, cam_y))


class Enemy:
    def __init__(self, x, y, difficulty=1):
        self.images_run = [pygame.image.load(f"ZOMBIE-PROJECT/zombie/character_zombie_run{i}.png").convert_alpha() for i in range(3)]
        self.image_idle = pygame.image.load("ZOMBIE-PROJECT/zombie/character_zombie_side.png").convert_alpha()
        self.image_jump = pygame.image.load("ZOMBIE-PROJECT/zombie/character_zombie_jump.png").convert_alpha()

        self.image = self.image_idle
        self.flip = False
        self.frame_index = 0
        self.animation_timer = 0

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = 2 * difficulty
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.jump_power = -10
        self.health = difficulty
        self.vision_range = 250
        self.difficulty = difficulty

    def can_see_player(self, player):
        distance = math.hypot(self.rect.centerx - player.rect.centerx,
                              self.rect.centery - player.rect.centery)
        return distance < self.vision_range

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def collide_with_platforms(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.bottom
                    self.velocity_y = 0

    def update_animation(self):
        if not self.on_ground:
            self.image = self.image_jump
        elif self.moving:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.images_run)
            self.image = self.images_run[self.frame_index]
        else:
            self.image = self.image_idle

    def update(self, player, platforms):
        self.apply_gravity()
        self.collide_with_platforms(platforms)

        self.moving = False

        if self.can_see_player(player):
            if player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed_x
                self.flip = True
                self.moving = True
            elif player.rect.centerx > self.rect.centerx:
                self.rect.x += self.speed_x
                self.flip = False
                self.moving = True

            if self.on_ground and player.rect.bottom < self.rect.top - 10:
                self.velocity_y = self.jump_power

            if self.on_ground:
                check_point = (self.rect.centerx, self.rect.bottom + 5)
                supported = any(p.collidepoint(check_point) for p in platforms)
                if not supported:
                    self.rect.x -= self.speed_x

        self.update_animation()

    def draw(self, screen, cam_x, cam_y):
        if self.health > 0:
            img = pygame.transform.flip(self.image, self.flip, False)
            screen.blit(img, (self.rect.x - cam_x, self.rect.y - cam_y))



class ShopItem:
    def __init__(self, weapon, price):
        self.weapon = weapon
        self.price = price



class DialogueManager:
    def __init__(self, dialogue_file):
        with open(dialogue_file, 'r', encoding='utf-8') as f:
            self.dialogue = json.load(f)
        self.current_node = "start"
        self.font = pygame.font.SysFont("Arial", 28)
        self.selection = 0
        self.dialogue_height = 400
        self.last_node = None
        self.saved_state = None
        self.sound = 0
        self.weapons = {
            "ak47": Weapon("AK-47", 2, 10, 120, ORANGE, 15, 5, True, 23000),
            "mosina": Weapon("Мосина", 10, 0.5, 10, PURPLE, 20, 0, False, 20000),
            "p90": Weapon("P90", 1, 15, 60, GREEN, 10, 10, True, 15000),
            "knife": Weapon("Нож", 3, 1, 999, GRAY, 5, 0, False, 5000)
        }

    def get_current_text(self):
        if "buy-" in self.current_node:
            self.current_node = "start"
        return self.dialogue[self.current_node]["text"]

    def get_current_choices(self):
        if "buy-" in self.current_node:
            self.current_node = "start"
        return list(self.dialogue[self.current_node]["choices"].keys())

    def play_voice(self):
        if "buy-" in self.current_node:
            self.current_node = "start"
        voice_file = self.dialogue[self.current_node].get("voice")
        if voice_file:
            try:
                if not self.sound == 0:
                    self.sound.stop()
                self.sound = pygame.mixer.Sound(f"ZOMBIE-PROJECT/voices/{voice_file}")
                self.sound.play()
            except:
                print(f"Не удалось загрузить звук: ZOMBIE-PROJECT/voices/{voice_file}")

    def choose(self, choice_index):
        choices = self.get_current_choices()
        if 0 <= choice_index < len(choices):
            choice_text = choices[choice_index]
            next_node = self.dialogue[self.current_node]["choices"].get(choice_text)

            if next_node and next_node.startswith("buy-"):
                item_type = next_node[4:]
                if item_type == "heal":
                    if player.money >= 2500:
                        player.money -= 2500
                        player.health = min(player.max_health, player.health + 50)
                        print("Куплена аптечка!")
                    else:
                        print("Недостаточно денег!")
                    return False
                elif item_type in self.weapons:
                    weapon = self.weapons[item_type]
                    if player.money >= weapon.price:
                        if player.add_weapon(weapon):
                            player.money -= weapon.price
                            print(f"Куплено {weapon.name} за ${weapon.price}")
                        else:
                            print("Нет свободных слотов для оружия!")
                    else:
                        print("Недостаточно денег!")
                    self.current_node = "start"
                    return False

            if next_node and next_node.startswith("target-"):
                target_name = next_node[7:]
                print(f"Установлена новая цель: {target_name}")
                self.last_node = self.current_node
                self.current_node = "start"
                return False

            elif next_node and next_node.startswith("goto-"):
                coords = next_node[5:].split('_')
                if len(coords) == 2:
                    x, y = map(int, coords)
                    print(f"Телепортация на координаты: {x}, {y}")
                self.last_node = self.current_node
                self.current_node = "start"
                return False

            elif next_node and next_node == "exit":
                self.current_node = "exit"
                return True

            elif next_node and next_node == "save_exit":
                if not self.sound == 0:
                    self.sound.stop()
                return True

            elif next_node:
                self.last_node = self.current_node
                self.current_node = next_node
                self.play_voice()
                return False

        return False

    def draw(self, screen):
        dialogue_rect = pygame.Rect(50, 50, WIDTH - 100, self.dialogue_height)
        pygame.draw.rect(screen, DIALOGUE_BG, dialogue_rect)
        pygame.draw.rect(screen, DIALOGUE_BORDER, dialogue_rect, 3)

        draw_text(screen, self.get_current_text(), self.font, WHITE, 70, 70, WIDTH - 140)

        choices = self.get_current_choices()
        if choices:
            start_y = 70 + self.font.get_height() * (len(self.get_current_text()) // (WIDTH - 140) + 1) + 20

            for i, choice in enumerate(choices):
                color = GREEN if i == self.selection else WHITE
                prefix = "> " if i == self.selection else "  "
                text_surface = self.font.render(f"{prefix}{choice}", True, color)
                screen.blit(text_surface, (70, start_y + i * 30))

    def restore_state(self):
        """Восстанавливает сохраненное состояние диалога"""
        if self.saved_state:
            self.current_node = self.saved_state['current_node']
            self.selection = self.saved_state['selection']

    def save_state(self):
        """Сохраняет текущее состояние диалога"""
        self.saved_state = {
            'current_node': self.current_node,
            'selection': self.selection
        }

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            choices = self.get_current_choices()

            if event.key == pygame.K_UP and choices:
                self.selection = (self.selection - 1) % len(choices)
                return False

            elif event.key == pygame.K_DOWN and choices:
                self.selection = (self.selection + 1) % len(choices)
                return False

            elif event.key == pygame.K_RETURN and choices:
                return self.choose(self.selection)

            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4) and choices:
                idx = event.key - pygame.K_1
                if idx < len(choices):
                    return self.choose(idx)

        return False

    def reset_dialogue(self):
        self.current_node = "start"
        self.selection = 0


class NPC:
    def __init__(self, x, y, dialogue_file, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dialogue = DialogueManager(dialogue_file)
        self.show_prompt = False
        self.interacting = False


    def update(self, player):
        self.show_prompt = self.rect.colliderect(player.rect.inflate(50, 50))
        keys = pygame.key.get_pressed()

        if self.show_prompt and keys[pygame.K_e]:
            if not self.interacting:
                self.interacting = True
                player.can_move = False
                self.dialogue.restore_state()
                self.dialogue.play_voice()
                pygame.time.wait(300)
            else:
                self.dialogue.play_voice()
                pygame.time.wait(300)

    def draw(self, screen, cam_x, cam_y):
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y - cam_y))

        if self.show_prompt and not self.interacting:
            font = pygame.font.SysFont("Benzin", 24)
            prompt = font.render("Нажмите E для взаимодействия", True, WHITE)
            screen.blit(prompt, (self.rect.x - cam_x, self.rect.y - 30 - cam_y))

        if self.interacting:
            self.dialogue.draw(screen)

    def handle_events(self, event, player):
        if self.interacting:
            should_close = self.dialogue.handle_input(event)
            if should_close:
                self.interacting = False
                player.can_move = True
                self.dialogue.save_state()
                return True
        return False

class Effect:
    def __init__(self, pos, text=""):
        self.pos = pos
        self.timer = 0
        self.text = text
        self.color = (random.randint(200,255), random.randint(0,50), random.randint(0,50))

effects = []

if not os.path.exists("ZOMBIE-PROJECT/npc_dialogues"):
    os.makedirs("ZOMBIE-PROJECT/npc_dialogues")

leha = {
    "start": {
        "text": "О, привет. Наконец-то проснулся. У нас сейчас все очень плохо. Зомби захватили уже процентов 60 нашего города, сейчас лагерь в котором мы находимся - одно из десяти безопасных мест во всей стране.",
        "voice": "dialog1.ogg",
        "choices": {
            "Что нам делать?": "whatidoing",
            "У нас есть оружие?": "guns",
            "Это очень страшно, я пока пойду осмотрюсь": "save_exit",
        }
    },
    "whatidoing": {
        "text": "Нужно проникнуть на место источника заражения, если мы его уничтожим - зомби больше не будут появляться.",
        "voice": "dialog2.ogg",
        "choices": {
            "У нас есть оружие?": "guns",
            "Спасибо за информацию, пойду осмотрюсь.": "save_exit",
        }
    },
    "guns": {
        "text": "Да, мой напарник Коротов продает его под этой лестницей, можешь зайти и что-нибудь взять. Из твоих денег, к сожелению, сохранилось только 10.000 рублей.",
        "voice": "dialog3.ogg",
        "choices": {
            "Что нам делать?": "whatidoing",
            "Пойду зайду к нему": "save_exit",
        }
    },
    "save_exit": {
        "text": "Я сохраню наш разговор. Возвращайся!",
        "voice": "dialog4.ogg",
        "choices": {}
    },
    "exit": {
        "text": "До встречи! (Диалог начнется сначала)",
        "voice": "dialog5.ogg",
        "choices": {}
    }
}

with open("ZOMBIE-PROJECT/npc_dialogues/npc1.json", 'w', encoding='utf-8') as f:
    json.dump(leha, f, ensure_ascii=False, indent=4)

player = Player(0, 100, 50, 50)

platforms = []
platforms.append(pygame.Rect(0, 500, 40000, 20))

for i in range(5):
    platforms.append(pygame.Rect(1000 + i * 80, 500 - i * 60, 60, 20))

platforms.append(pygame.Rect(1400, 200, 300, 20))
platforms.append(pygame.Rect(1300, 400, 500, 20))

platforms.append(pygame.Rect(1800, 500, 400, 20))
platforms.append(pygame.Rect(2180, 300, 20, 200))
platforms.append(pygame.Rect(1800, 300, 300, 20))

for i in range(30):
    y_offset = math.sin(i * 0.3) * 50
    platforms.append(pygame.Rect(2200 + i * 120, 400 + y_offset, 100, 20))

building2_rect = pygame.Rect(5000, 200, 600, 300)
platforms.append(pygame.Rect(5000, 500, 600, 20))
platforms.append(pygame.Rect(5000, 200, 20, 300))
platforms.append(pygame.Rect(5580, 200, 20, 300))

npcs = [
    NPC(1600, 150, "ZOMBIE-PROJECT/npc_dialogues/npc1.json", "ZOMBIE-PROJECT/npc/character_robot_side.png"),
    NPC(1500, 150, "ZOMBIE-PROJECT/npc_dialogues/npc2.json", "ZOMBIE-PROJECT/npc/character_robot_side.png"),
    NPC(1600, 350, "ZOMBIE-PROJECT/npc_dialogues/npc3.json", "ZOMBIE-PROJECT/npc/character_robot_side.png")
]

enemies = []
for i in range(50):
    x = 2500 + i * 150
    y = 300 + math.sin(i) * 50
    difficulty = min(5, 1 + i // 5)
    enemies.append(Enemy(x, y, difficulty))

for i in range(20):
    x = 5100 + (i % 10) * 50
    y = 450 - (i // 10) * 60
    enemies.append(Enemy(x, y, 3))

for i in enemies:
    effects.append(Effect(i.rect.center, f"+{100 * kill_streak}"))

boss = Enemy(5400, 400, 10)
boss.health = 20
boss.speed_x = 4
boss.rect = pygame.Rect(5400, 400, 80, 100)
enemies.append(boss)

bullets = []
running = True
game_state = "start"
old_sound_name = 0

while running:
    current_time = pygame.time.get_ticks()

    if slow_motion and current_time - slow_start > slow_duration:
        slow_motion = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        dialog_closed = False
        for npc in npcs:
            if npc.interacting:
                dialog_closed = npc.handle_events(event, player)
                if dialog_closed:
                    break

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if player.current_weapon and player.current_weapon.ammo > 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            target_x = mouse_x + player.rect.centerx - WIDTH // 2
            target_y = mouse_y + player.rect.centery - HEIGHT // 2

            new_bullets = player.current_weapon.shoot(
                player.rect.centerx, player.rect.centery,
                target_x, target_y,
                current_time
            )
            bullets.extend(new_bullets)

    if pygame.mouse.get_pressed()[0] and player.current_weapon and player.current_weapon.auto:
        if player.current_weapon.ammo > 0 and player.current_weapon.can_shoot(current_time):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            target_x = mouse_x + player.rect.centerx - WIDTH // 2
            target_y = mouse_y + player.rect.centery - HEIGHT // 2

            new_bullets = player.current_weapon.shoot(
                player.rect.centerx, player.rect.centery,
                target_x, target_y,
                current_time
            )
            bullets.extend(new_bullets)

    if not(player.current_weapon is None) and player.current_weapon.ammo <= 0:
        player.weapons.remove(player.current_weapon)
        if player.weapons:
            player.current_weapon = player.weapons[0]
        else:
            player.current_weapon = None

    screen.fill(BLACK)
    player.move(platforms)
    cam_x = player.rect.centerx - WIDTH // 2
    cam_y = player.rect.centery - HEIGHT // 2

    background.update(player.rect.centerx, player.rect.centery)
    background.draw(screen, cam_x, cam_y)

    for effect in effects[:]:
        effect.timer += 1
        if effect.timer > 60:
            effects.remove(effect)
        else:
            font = pygame.font.SysFont("Arial", 20 + effect.timer // 2)
            text = font.render(effect.text, True, effect.color)
            pos = (effect.pos[0]-cam_x, effect.pos[1]-cam_y)+ (0, -effect.timer * 2)
            screen.blit(text, pos)

    for plat in platforms:
        screen_platform = plat.move(-cam_x, -cam_y)
        pygame.draw.rect(screen, (100, 100, 100), screen_platform)

    for npc in npcs:
        npc.update(player)
        npc.draw(screen, cam_x, cam_y)

    player.draw(screen, cam_x, cam_y)


    for enemy in enemies:
        enemy.update(player, platforms)
        enemy.draw(screen, cam_x, cam_y)

        if player.rect.colliderect(enemy.rect):
            damage = 1
            if enemy == boss:
                damage = 5
            player.health -= damage

            direction_x = player.rect.centerx - enemy.rect.centerx
            direction_y = player.rect.centery - enemy.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance != 0:
                direction_x /= distance
                direction_y /= distance
                knockback = 15 if enemy == boss else 10
                player.rect.x += direction_x * knockback
                player.rect.y += direction_y * knockback

                for platform in platforms:
                    if player.rect.colliderect(platform):
                        if direction_y > 0:
                            player.rect.bottom = platform.top
                            player.vel_y = 0
                            player.on_ground = True
                        elif direction_y < 0:
                            player.rect.top = platform.bottom
                            player.vel_y = 0

            if player.health <= 0:
                print("[!] Игрок погиб. Игра окончена.")
                running = False

    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen, cam_x, cam_y)

        if not (0 <= bullet.rect.x <= 6000 and 0 <= bullet.rect.y <= 6000):
            bullets.remove(bullet)
            continue

        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemy.health -= 1
                bullets.remove(bullet)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    kill_streak += 1
                    last_kill = current_time
                    player.money += 500
                    if kill_streak >= 2:
                        slow_motion = True
                        slow_start = current_time
                        combo_alpha = 255
                        combo_text = f"{kill_streak}X COMBO!"
                        old_combo = kill_streak
                        if kill_streak <= 5:
                            sound_name = kill_streak
                        elif 10 > kill_streak > 5:
                            sound_name = 6
                        elif 15 > kill_streak > 9:
                            sound_name = 10
                        elif kill_streak > 14:
                            sound_name = 15
                        if old_sound_name != sound_name:
                            if steak_sound:
                                sound = pygame.mixer.Sound(f"ZOMBIE-PROJECT/steaks/{sound_name}.mp3")
                                sound.play()
                        player.money += 50 * kill_streak
                        old_sound_name = sound_name
                    if enemy == boss:
                        print("Босс побежден!")
                        npcs[2].rect.x = 5600
                break

    if current_time - last_kill > 3000:
        kill_streak = 0

    if combo_alpha > 0:
        font = pygame.font.SysFont("Benzin", 40 + int(combo_alpha / 10))
        text = font.render(combo_text, True, (255, 50, 50, combo_alpha))
        text.set_alpha(combo_alpha)
        screen.blit(text, (WIDTH // 2 - text.get_width() / 2, HEIGHT // 3))
        combo_alpha = max(0, combo_alpha - 3)

    if slow_motion:
        dt = 40
    else:
        dt = 60

    if boss not in enemies and player.rect.colliderect(pygame.Rect(5600, 450, 40, 60)):
        print("Уровень пройден!")
        running = False

    draw_hud(screen, player)

    pygame.display.flip()
    clock.tick(dt)

pygame.quit()