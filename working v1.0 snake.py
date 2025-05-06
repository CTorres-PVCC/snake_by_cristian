import pygame
import sys
import time
from pygame.math import Vector2

# Constants
BACKGROUND_COLOR = (189,236,172)  # Light green background
import random
class Snake:
    def __init__(self, cell_size, cell_number):
        self.cell_size = cell_size
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()    
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()   
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        
     
        
    def draw_snake(self, screen):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * self.cell_size)
            y_pos = int(block.y * self.cell_size)
            block_rect = pygame.Rect(x_pos, y_pos,self.cell_size,self.cell_size)   
            
            if index == 0:
                screen.blit(self.head,block_rect)  
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)  
            
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                elif previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                    screen.blit(self.body_tl,block_rect)
                elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                    screen.blit(self.body_bl,block_rect)
                elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                    screen.blit(self.body_tr,block_rect)
                elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                    screen.blit(self.body_br,block_rect)     

    def update_head_graphics(self):
        if len(self.body) > 1:
            head_relation = self.body[1] - self.body[0] 
            if head_relation == Vector2(1, 0): self.head = self.head_left
            elif head_relation == Vector2(-1, 0): self.head = self.head_right
            elif head_relation == Vector2(0, 1): self.head = self.head_up
            elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down  

    

        #    snake_rect = pygame.Rect(segment.x * self.cell_size, segment.y * self.cell_size, self.cell_size, self.cell_size)
        #    pygame.draw.rect(screen, (139,69,19), snake_rect)
   
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
         
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self, screen):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        
       


class Fruit:
    def __init__(self, cell_size, apple_image):
        self.randomize()
        self.cell_size = cell_size
        self.apple_image = apple_image

    def draw(self, screen):
        fruit_rect = pygame.Rect(self.position.x * self.cell_size, self.position.y * self.cell_size, self.cell_size, self.cell_size)
        screen.blit(self.apple_image, fruit_rect)
        # pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def randomize(self):
         self.x = random.randint(0, cell_number - 1)
         self.y = random.randint(0, cell_number - 1)
         self.position = Vector2(self.x, self.y)    

class Main:
    def __init__(self):
        self.snake = Snake(cell_size, cell_number)
        self.fruit = Fruit(cell_size, apple)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self, screen):
        self.draw_grass(screen)
        self.snake.draw_snake(screen)
        self.fruit.draw(screen)
        self.draw_score(screen)

    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.position:
                self.fruit.randomize()
                self.snake.add_block()
                self.snake.play_crunch_sound()
                break    

    def check_fail(self):
       if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
           self.game_over()

       for block in self.snake.body[1:]:
           if block == self.snake.body[0]:
               self.game_over()  

    def draw_grass(self, screen):
        grass_color = (102, 200, 102)
        
        for col in range(cell_number):
            for row in range(cell_number):
                    if (row + col) % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            pygame.draw.rect(screen, grass_color, grass_rect)

    def game_over(self):
        score_text = len(self.snake.body) - 3  # Calculate the score based on the snake's body length
        game_over_surface = game_font.render(f'Game Over! Score: {score_text} Press R to Reset', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()  # Update the display to show the game over message
        wait_for_reset = True
        while wait_for_reset:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        self.snake.reset(screen)
                    if event.key == pygame.K_r:
                        wait_for_reset = False
         
        #self.snake.reset(screen)  # Reset the snake to its initial state

    def draw_score(self, screen): 
        score_text = len(self.snake.body) - 3  # Subtracting the initial length of the snake
        score_surface = game_font.render(f'Score: {score_text}', True, (0, 0, 0)) 
        score_x = int(cell_size * cell_number - 60)  # Positioning score at the top right corner
        score_y = int(cell_size * cell_number - 40)  # Positioning score at the top right corner
        score_rect = score_surface.get_rect(center = (score_x, score_y))  # Centering the score text
        screen.blit(score_surface,score_rect)  # Display score at the top left corner 
                    
                

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption('Snake Game By Cristian')
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()  # Load an apple image 
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

main_game = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN :
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_r:
                main_game.snake.reset(screen) 
                       

    screen.fill((120,229,131))  #` Clear the screen with a light green color
    main_game.draw_elements(screen)
    pygame.display.update()
    clock.tick(30)  # Control the frame rate