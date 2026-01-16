import pygame
import sys

# ================= CONFIG =================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

GRID_WIDTH = 20
GRID_HEIGHT = 15

# Tile types
TILES = {
    'Empty': '0',
    'Wall': '1',
    'Blue': '2',
    'Red': '3',
    'Goal': '4',
    'Spike': '5',
    'Player': 'P'
}

# Colors
COLORS = {
    '0': (0, 0, 0),
    '1': (50, 50, 50),
    '2': (0, 170, 255),
    '3': (240, 5, 85),
    '4': (0, 255, 0),
    '5': (255, 0, 0),
    'P': (255, 255, 0)
}

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Paradox Prism Level Editor")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 16)

# ================= TILE SIZE =================
def recalc_tile_size():
    global TILE_SIZE
    TILE_SIZE = min(
        WINDOW_WIDTH // GRID_WIDTH,
        WINDOW_HEIGHT // GRID_HEIGHT
    )
    TILE_SIZE = max(8, TILE_SIZE)

recalc_tile_size()

# ================= GRID =================
grid = [['0' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_tile = '1'

# ================= BUTTON =================
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)
        txt = font.render(self.text, True, (0, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# ================= GRID RESIZE =================
def resize_grid(new_w, new_h):
    global grid, GRID_WIDTH, GRID_HEIGHT

    new_w = max(5, new_w)
    new_h = max(5, new_h)

    new_grid = [['0' for _ in range(new_w)] for _ in range(new_h)]

    for y in range(min(GRID_HEIGHT, new_h)):
        for x in range(min(GRID_WIDTH, new_w)):
            new_grid[y][x] = grid[y][x]

    GRID_WIDTH = new_w
    GRID_HEIGHT = new_h
    grid = new_grid
    recalc_tile_size()

def inc_w(): resize_grid(GRID_WIDTH + 5, GRID_HEIGHT)
def dec_w(): resize_grid(GRID_WIDTH - 5, GRID_HEIGHT)
def inc_h(): resize_grid(GRID_WIDTH, GRID_HEIGHT + 5)
def dec_h(): resize_grid(GRID_WIDTH, GRID_HEIGHT - 5)

buttons = [
    Button(10, 10, 50, 25, "+W", inc_w),
    Button(65, 10, 50, 25, "-W", dec_w),
    Button(120, 10, 50, 25, "+H", inc_h),
    Button(175, 10, 50, 25, "-H", dec_h),
]

# ================= DRAW =================
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = grid[y][x]
            color = COLORS[tile]
            pygame.draw.rect(
                screen,
                color,
                (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
            pygame.draw.rect(
                screen,
                (40, 40, 40),
                (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                1
            )

def export_level():
    print("\n--- COPY THIS LEVEL INTO YOUR JS ---\n")
    print("[")
    for row in grid:
        print(f"\"{''.join(row)}\",")
    print("]")
    print("\n-----------------------------------\n")

# ================= LOOP =================
running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid()

    for b in buttons:
        b.draw()

    info = font.render(
        f"Tile: {current_tile} | Size: {GRID_WIDTH}x{GRID_HEIGHT}",
        True,
        (0, 255, 255)
    )
    screen.blit(info, (10, WINDOW_HEIGHT - 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_tile = '1'
            elif event.key == pygame.K_2: current_tile = '2'
            elif event.key == pygame.K_3: current_tile = '3'
            elif event.key == pygame.K_4: current_tile = '4'
            elif event.key == pygame.K_5: current_tile = '5'
            elif event.key == pygame.K_6: current_tile = 'P'
            elif event.key == pygame.K_0: current_tile = '0'
            elif event.key == pygame.K_s: export_level()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for b in buttons:
                b.click(event.pos)

            mx, my = event.pos
            gx = mx // TILE_SIZE
            gy = my // TILE_SIZE

            if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                if current_tile == 'P':
                    for y in range(GRID_HEIGHT):
                        for x in range(GRID_WIDTH):
                            if grid[y][x] == 'P':
                                grid[y][x] = '0'
                grid[gy][gx] = current_tile

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = event.pos
            gx = mx // TILE_SIZE
            gy = my // TILE_SIZE
            if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                grid[gy][gx] = '0'

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
