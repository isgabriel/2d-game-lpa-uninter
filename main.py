import pygame
from config import WIDTH, HEIGHT, FPS
from utils import get_background
from player import Player
from objects import Block, Fire, EndSign
from collisions import handle_move
from level import build_platforms


pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))


def draw(win, background, bg_image, player, objects, offset_x):
    for tile in background:
        win.blit(bg_image, tile)

    for obj in objects:
        obj.draw(win, offset_x)

    player.draw(win, offset_x)
    pygame.display.update()


def main() -> None:
    clock = pygame.time.Clock()
    background, bg_image = get_background("Pink.png")

    block_size = 96

    player = Player(0, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()

    platforms, last_platform_x = build_platforms(block_size, HEIGHT)

    floor = [
        Block(i * block_size, HEIGHT - block_size, block_size)
        for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)
    ]

    extended_floor_len = 10
    extended_floor = [
        Block(last_platform_x + i * block_size, HEIGHT - block_size, block_size)
        for i in range(extended_floor_len)
    ]

    end_x = last_platform_x + (extended_floor_len - 1) * block_size
    end_sign = EndSign(end_x, HEIGHT - block_size - 50)

    wall_x = last_platform_x + extended_floor_len * block_size
    wall_blocks = [
        Block(wall_x, HEIGHT - block_size - i * block_size, block_size)
        for i in range(1, 9)
    ]

    objects = [
        *floor,
        *platforms,
        *extended_floor,
        *wall_blocks,
        end_sign,
        Block(0, HEIGHT - block_size * 2, block_size),
        Block(block_size * 2, HEIGHT - block_size * 3, block_size),
        Block(block_size * 3, HEIGHT - block_size * 4, block_size),
        fire,
    ]

    offset_x = 0
    scroll_area_width = 200

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)

        if (
            player.rect.right - offset_x >= WIDTH - scroll_area_width
            and player.x_vel > 0
        ) or (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
            offset_x += player.x_vel

        if player.rect.top > HEIGHT:
            player.rect.x, player.rect.y = 100, 100
            player.x_vel = player.y_vel = 0
            player.fall_count = player.jump_count = 0
            offset_x = 0

        draw(window, background, bg_image, player, objects, offset_x)

    pygame.quit()


if __name__ == "__main__":
    main()
