import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Definir constantes
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 10

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
EDGAR_BLUE = (0, 128, 255)

# Clase para representar la serpiente
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.grow = False

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= GRID_SIZE
        elif self.direction == "DOWN":
            y += GRID_SIZE
        elif self.direction == "LEFT":
            x -= GRID_SIZE
        elif self.direction == "RIGHT":
            x += GRID_SIZE

        # Añadir nueva cabeza
        self.body.insert(0, (x, y))

        # Si no ha comido, eliminar la cola
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, RED, (*segment, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE, (*segment, GRID_SIZE, GRID_SIZE), 1)

        # Dibujar cabeza de la serpiente
        pygame.draw.rect(surface, BLACK, (*self.body[0], GRID_SIZE, GRID_SIZE))


# Clase para representar la comida
class Banana:
    def __init__(self):
        self.x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE

    def draw(self, surface):
        banana_img = pygame.image.load('banana.png').convert_alpha()
        surface.blit(banana_img, (self.x, self.y))


# Función para mostrar la pantalla de game over
def show_game_over_screen(screen):
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, RED)
    continue_text = font.render("Press 'C' to Continue", True, WHITE)
    restart_text = font.render("Press 'R' to Restart", True, WHITE)
    exit_text = font.render("Press 'X' to Exit", True, WHITE)
    edgarsntn_text = font.render("edgarsntn", True, EDGAR_BLUE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(edgarsntn_text, (10, HEIGHT - 30))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return True
                elif event.key == pygame.K_r:
                    return False
                elif event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()


# Función principal del juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    while True:
        snake = Snake()
        banana = Banana()

        running = True
        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != "DOWN":
                        snake.direction = "UP"
                    elif event.key == pygame.K_DOWN and snake.direction != "UP":
                        snake.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                        snake.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                        snake.direction = "RIGHT"

            snake.move()

            # Verificar colisiones
            if (snake.body[0][0] == banana.x and snake.body[0][1] == banana.y):
                snake.grow_snake()
                banana = Banana()

            # Verificar colisiones con las paredes
            if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
                snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT):
                running = False

            # Verificar colisiones con el propio cuerpo
            if len(snake.body) > 1 and snake.body[0] in snake.body[1:]:
                running = False

            snake.draw(screen)
            banana.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

        if not show_game_over_screen(screen):
            continue
        else:
            break

if __name__ == "__main__":
    main()
