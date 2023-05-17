import pygame
import sys
import math

pygame.init()

# Values
w_w = 350
w_h = 600
window = pygame.display.set_mode((w_w, w_h))
pygame.display.set_caption("Tower Blocks Game")

font_large = pygame.font.Font(None, 35)
font_medium = pygame.font.Font(None, 25)

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

game_active = False
difficulty_level = 1
menu_active = True

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (w_w, w_h))
background1_image = pygame.image.load("background(1).png")
background1_image = pygame.transform.scale(background1_image, (w_w, w_h))
block_image = pygame.image.load("block.png")
block_image = pygame.transform.scale(block_image, (50, 50))
platform_image = pygame.image.load("platform.png")
platform_image = pygame.transform.scale(platform_image, (50, 50))


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.font = font_medium
        self.color = white
        self.x = x
        self.y = y
        self.width = 200
        self.height = 50

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, black)
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        window.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height


block_w = 50
block_h = 50
block_x = w_w // 2 - block_w // 2
block_y = w_h // 2 - block_h // 2
block_angle = math.radians(60)
block_rotation_speed = 0.02

rope_length = 240 * 0.4
rope_height = rope_length
rope_angle = 0
rope_angle_speed = 0.02
rope_direction = 1
gravity = 0.5
block_falling = False

start_button = Button("Start Game", w_w // 2 - 100, 200)
difficulty_button = Button("Difficulty Level", w_w // 2 - 100, 260)
quit_button = Button("Quit Game", w_w // 2 - 100, 320)

clock = pygame.time.Clock()

# Here my game loop starts
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_active:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    game_active = True
                    menu_active = False
                elif difficulty_button.is_clicked(mouse_pos):
                    pass
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif game_active:
                block_falling = True

    window.fill(black)

    if menu_active:
        window.blit(background_image, (0, 0))
        menu_title = font_large.render("Tower Blocks", True, white)

        start_button.color = white
        difficulty_button.color = white
        quit_button.color = white

        mouse_pos = pygame.mouse.get_pos()
        if start_button.is_clicked(mouse_pos):
            start_button.color = gray
        elif difficulty_button.is_clicked(mouse_pos):
            difficulty_button.color = gray
        elif quit_button.is_clicked(mouse_pos):
            quit_button.color = gray

        start_button.draw()
        difficulty_button.draw()
        quit_button.draw()
        window.blit(menu_title, (w_w // 2 - menu_title.get_width() // 2, 100))

    elif game_active:
        window.blit(background1_image, (0, 0))
        window.blit(platform_image, (w_w // 2 - 25, w_h - 50))

        if block_falling:
            block_y += gravity
            gravity += 0.2

        rope_angle += rope_direction * rope_angle_speed

        if rope_angle >= math.pi / 2.7:
            rope_direction = -1
        elif rope_angle <= -math.pi / 2.7:
            rope_direction = 1

        block_center_x = w_w // 2
        block_center_y = rope_height
        block_x = block_center_x - block_w // 2 + int(rope_length * math.sin(rope_angle))
        block_y = min(block_y, w_h - block_h)

        window.blit(block_image, (block_x, block_y))

        pygame.draw.line(window, white, (block_center_x, 0), (block_x + block_w // 2, block_y), 5)

    pygame.display.flip()
    clock.tick(60)
