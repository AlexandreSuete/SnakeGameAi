import random
import sys

import pygame

# Inicializa o Pygame
pygame.init()

# Constantes
CELL_SIZE = 30
GRID_SIZE = 16 #precisa ser par
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FPS = 18
BORDER_SIZE = 1
TOTAL_CELLS = GRID_SIZE * GRID_SIZE

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Enums
class Direction:
    up, down, left, right = range(4)

def interpolate_color(color1, color2, factor):
    """ Interpola entre duas cores. """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return r, g, b

#Realizando lógica da Heuristica
def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

#Lógica do A*
def a_star_search(start, goal, grid, snake_tail):
    open_set = set()
    closed_set = set()
    open_set.add(start)

    came_from = {}
    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float('inf') for row in grid for cell in row}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda cell: f_score[cell])

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Retorna o caminho invertido

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in current.get_neighbors(grid, snake_tail):  # Usa o método get_neighbors para analisar se os vizinhos podem ou não serem usados
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 1  

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    return []


# Classe Snake
class Snake:
    def __init__(self, grid):
        self.x = random.randint(0, GRID_SIZE - 1)
        self.y = random.randint(0, GRID_SIZE - 1)
        self.grid = grid
        self.length = 1
        self.tail = [(self.x, self.y)]

        # Define a direção inicial com base nas propriedades da célula inicial
        cell = self.grid[self.y][self.x]
        directions = []
        if cell.up: directions.append(Direction.up)
        if cell.down: directions.append(Direction.down)
        if cell.left: directions.append(Direction.left)
        if cell.right: directions.append(Direction.right)

        self.direction = random.choice(directions) if directions else None

    #Lógica da movimentação da cobra
    def move(self, food):
        cell = self.grid[self.y][self.x]

        # Tenta encontrar um caminho usando o A*
        start = cell
        goal = self.grid[food.y][food.x]
        path = a_star_search(start, goal, grid, self.tail)


        if path:
            #Caso o caminho seja encontrado, move a cobra para a próxima célula do A*
            next_step = path[0]
            self.x, self.y = next_step.x, next_step.y
        else:
            #Lógica para quando não há caminho
            directions = []
             #move para a direção com mais vizinhos ocupados
            if cell.up and (self.x, self.y - 1) not in self.tail:
                directions.append((Direction.up, self.count_body_neighbors(self.x, self.y - 1, self.grid)))
            if cell.down and (self.x, self.y + 1) not in self.tail:
                directions.append((Direction.down, self.count_body_neighbors(self.x, self.y + 1, self.grid)))
            if cell.left and (self.x - 1, self.y) not in self.tail:
                directions.append((Direction.left, self.count_body_neighbors(self.x - 1, self.y, self.grid)))
            if cell.right and (self.x + 1, self.y) not in self.tail:
                directions.append((Direction.right, self.count_body_neighbors(self.x + 1, self.y, self.grid)))
                
            if directions:
                self.direction, _ = max(directions, key=lambda x: x[1])

            # Move a cobra na direção escolhida
            if self.direction == Direction.up:
                self.y -= 1
            elif self.direction == Direction.down:
                self.y += 1
            elif self.direction == Direction.left:
                self.x -= 1
            elif self.direction == Direction.right:
                self.x += 1

        # Atualiza a cauda da cobra
        self.tail.append((self.x, self.y))
        if len(self.tail) > self.length:
            del self.tail[0]
    #Conta os vizinhos que são ocupados pelo corpo da cobra        
    def count_body_neighbors(self, x, y, grid):
        count = 0
        if (x, y - 1) in self.tail:
            count += 1
        if (x, y + 1) in self.tail:
            count += 1
        if (x - 1, y) in self.tail:
            count += 1
        if (x + 1, y) in self.tail:
            count += 1
        return count
    #Desenha a cobra        
    def draw(self, window):
        tail_length = len(self.tail)
        for i, (x, y) in enumerate(self.tail):
            factor = i / max(1, tail_length - 1)

            # Interpola entre verde e azul
            color = interpolate_color(GREEN, BLUE, factor)

            snake_rect = pygame.Rect(
                x * CELL_SIZE + BORDER_SIZE,
                y * CELL_SIZE + BORDER_SIZE,
                CELL_SIZE - 2 * BORDER_SIZE,
                CELL_SIZE - 2 * BORDER_SIZE
            )
            pygame.draw.rect(window, color, snake_rect)

    def check_collision(self):
        if self.x < 0 or self.x >= GRID_SIZE or self.y < 0 or self.y >= GRID_SIZE:
            return True
        for x, y in self.tail[:-1]:
            if self.x == x and self.y == y:
                return True
        return False

    def check_food(self, food):
        if self.x == food.x and self.y == food.y:
            self.length += 1
            return True
        return False

    def check_direction(self, direction):
        if direction == Direction.up and self.direction != Direction.down:
            self.direction = direction
        elif direction == Direction.down and self.direction != Direction.up:
            self.direction = direction
        elif direction == Direction.left and self.direction != Direction.right:
            self.direction = direction
        elif direction == Direction.right and self.direction != Direction.left:
            self.direction = direction
#Classe food
class Food:
    def __init__(self, snake):
        self.x, self.y = self.generate_food_position(snake)
    #Gera a posição da comida
    def generate_food_position(self, snake):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in snake.tail:
                return x, y
    #Desenha a comida
    def draw(self, window):
        food_rect = pygame.Rect(
            self.x * CELL_SIZE + BORDER_SIZE,
            self.y * CELL_SIZE + BORDER_SIZE,
            CELL_SIZE - 2 * BORDER_SIZE,
            CELL_SIZE - 2 * BORDER_SIZE
        )
        pygame.draw.rect(window, RED, food_rect)

# Classe Cell
class Cell:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.up = False
        self.down = False
        self.left = False
        self.right = False
    #Retorna os vizinhos da célula    
    def get_neighbors(self, grid, snake_tail):
        neighbors = []
        if self.up and self.y > 0 and (self.x, self.y - 1) not in snake_tail:
            neighbors.append(grid[self.y - 1][self.x])
        if self.down and self.y < GRID_SIZE - 1 and (self.x, self.y + 1) not in snake_tail:
            neighbors.append(grid[self.y + 1][self.x])
        if self.left and self.x > 0 and (self.x - 1, self.y) not in snake_tail:
            neighbors.append(grid[self.y][self.x - 1])
        if self.right and self.x < GRID_SIZE - 1 and (self.x + 1, self.y) not in snake_tail:
            neighbors.append(grid[self.y][self.x + 1])
        return neighbors
    #Desenha a célula
    def draw(self, window):
        inner_rect = pygame.Rect(
            self.x * CELL_SIZE + BORDER_SIZE,
            self.y * CELL_SIZE + BORDER_SIZE,
            CELL_SIZE - 2 * BORDER_SIZE,
            CELL_SIZE - 2 * BORDER_SIZE
        )
        pygame.draw.rect(window, WHITE, inner_rect)
        mid_point = (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2)
        if self.up:
            pygame.draw.polygon(window, RED, [mid_point, (mid_point[0] - 3, mid_point[1] + 3), (mid_point[0] + 3, mid_point[1] + 3)])
        if self.down:
            pygame.draw.polygon(window, RED, [mid_point, (mid_point[0] - 3, mid_point[1] - 3), (mid_point[0] + 3, mid_point[1] - 3)])
        if self.left:
            pygame.draw.polygon(window, RED, [mid_point, (mid_point[0] + 3, mid_point[1] - 3), (mid_point[0] + 3, mid_point[1] + 3)])
        if self.right:
            pygame.draw.polygon(window, RED, [mid_point, (mid_point[0] - 3, mid_point[1] - 3), (mid_point[0] - 3, mid_point[1] + 3)])

# Inicializa a janela do jogo
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
grid = [[Cell(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
snake = Snake(grid)
food = Food(snake)
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
victory_message = font.render('Vitória!', True, (0, 255, 0))  # Verde

# Função para desenhar o grid
def draw_grid():
    #Lógica para definir quais são as direções possíveis para cada célula
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell = grid[y][x]
            if x % 2 == 0:  # Se x for par
                cell.down = True
            else:  # Se x for ímpar
                cell.up = True
            if y % 2 == 0:
                cell.left = True
            else:
                cell.right = True
                
            # Restrições para as bordas do grid
            if x == 0:
                cell.left = False
            if x == GRID_SIZE - 1:
                cell.right = False
            if y == 0:
                cell.up = False
            if y == GRID_SIZE - 1:
                cell.down = False
            #Desenha a célula    
            cell.draw(window)

# Loop principal do jogo
clock = pygame.time.Clock()

while True:
    #Loop para funcionamento do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if len(snake.tail) >= TOTAL_CELLS:
        snake = Snake(grid)
        food = Food(snake)
    else:
        window.fill(BLACK)
    if snake.check_collision():
        snake = Snake(grid)
    if snake.check_food(food):
        food = Food(snake)
    snake.move(food)
    
    draw_grid()
    snake.draw(window)
    food.draw(window)
    

    pygame.display.update()
    clock.tick(FPS)

if __name__ == '__main__':
    main()