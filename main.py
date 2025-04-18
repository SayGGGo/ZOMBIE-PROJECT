import os

from cfg import FPS
from os import environ
import time
import colorama
from colorama import Fore, Back, Style
import sys

colorama.init()

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

print(f"{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Style.RESET_ALL} {Fore.GREEN}Инициализация PYGAME...{Style.RESET_ALL}")
pygame.init()

print(f"{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Style.RESET_ALL} {Fore.GREEN}Загрузка классов и окна...{Style.RESET_ALL}")


class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.screen_rect = pygame.Rect(WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2, width,
                                       height)
        self.color = 255, 255, 255
        self.speed = 5

        self.x = x
        self.y = y

        self.is_jumping = False
        self.is_falling = False
        self.jump_velocity = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.ground_level = y + height

        self.can_jump = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.screen_rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        if keys[pygame.K_SPACE] and self.can_jump and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = self.jump_power
            self.can_jump = False

        if self.is_jumping or self.is_falling:
            self.jump_velocity += self.gravity
            self.y += self.jump_velocity

            if self.y + self.rect.height >= self.ground_level:
                self.y = self.ground_level - self.rect.height
                self.is_jumping = False
                self.is_falling = False
                self.jump_velocity = 0
                self.can_jump = True

            elif self.jump_velocity > 0:
                self.is_jumping = False
                self.is_falling = True

        self.rect.x = self.x
        self.rect.y = self.y


WIDTH = pygame.display.get_desktop_sizes()[0][0]
HEIGHT = pygame.display.get_desktop_sizes()[0][1]
DISPLAY_SIZE = pygame.display.get_desktop_sizes()[0]

screen = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()

player = Player(0, 0, 50, 50)
player.ground_level = 50

platforms = [
    pygame.Rect(-500, 50, 1000, 20),
    pygame.Rect(200, -50, 100, 20), 
    pygame.Rect(-300, -100, 100, 20)
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    player.move()

    for platform in platforms:
        screen_platform = platform.move(-player.x + WIDTH // 2 - player.rect.width // 2,
                                        -player.y + HEIGHT // 2 - player.rect.height // 2)
        pygame.draw.rect(screen, (100, 100, 100), screen_platform)

    player.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_PAGEUP]:
        print("\n"*100+f"{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Style.RESET_ALL} {Fore.GREEN}Игрок: {Fore.WHITE}{(player.x, player.y)}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Fore.GREEN} ZOMBIE PROJECT ОТ АНДРЕЯ САЙГИНА П-63")
        print(f"{Fore.LIGHTGREEN_EX}[ZOMBIE PROJECT]{Fore.GREEN} Откладка активируется на {Fore.WHITE}PAGE UP{Style.RESET_ALL}")
        input(f"\n{Fore.LIGHTGREEN_EX}[-]{Fore.GREEN} Нажмите {Fore.GREEN}ENTER{Fore.GREEN} чтобы продолжить...{Style.RESET_ALL}")

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()