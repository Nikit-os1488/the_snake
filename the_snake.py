import pygame
from random import choice

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

class GameObject:
    def __init__(self, position=(0, 0)):
        self.position = position
        self.body_color = None

    def draw(self):
        pass

class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        x_positions = [i * GRID_SIZE for i in range(GRID_WIDTH)]
        y_positions = [i * GRID_SIZE for i in range(GRID_HEIGHT)]
        self.position = (choice(x_positions), choice(y_positions))

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self):
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.length = 2
        self.positions = [self.position]
        self.direction = 'RIGHT'
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.positions[0]

        if self.direction == 'UP':
            head_y -= GRID_SIZE
        elif self.direction == 'DOWN':
            head_y += GRID_SIZE
        elif self.direction == 'LEFT':
            head_x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            head_x += GRID_SIZE

        if head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE
        elif head_x >= SCREEN_WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE
        elif head_y >= SCREEN_HEIGHT:
            head_y = 0

        self.positions = [(head_x, head_y)] + self.positions[:self.length - 1]

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.__init__()

    def draw(self):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                snake.next_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                snake.next_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                snake.next_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                snake.next_direction = 'RIGHT'

def main():
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(SPEED)
