import pygame
import sys

# --- CONFIG ---
TILE_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15
WINDOW_WIDTH = TILE_SIZE * GRID_WIDTH
WINDOW_HEIGHT = TILE_SIZE * GRID_HEIGHT
FPS = 60

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

# --- INITIALIZE ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Paradox Prism Level Editor")
clock = pygame.time.Clock()

# Grid (default empty)
grid = [['0' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_tile = '1'  # start with Wall

font = pygame.font.SysFont("Courier", 20)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = grid[y][x]
            color = COLORS[tile]
            pygame.draw.rect(screen, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (40, 40, 40), (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def export_level():
    lines = []
    for row in grid:
        lines.append('"' + ''.join(row) + '"')
    level_code = "[\n" + ",\n".join(lines) + "\n]"
    print("\n--- COPY THIS LEVEL INTO YOUR JS ---\n")
    print(level_code)
    print("\n-----------------------------------\n")

running = True
while running:
    screen.fill((0,0,0))
    draw_grid()
    
    # Display current tile
    txt_surface = font.render(f"Current Tile: {current_tile}", True, (0, 255, 255))
    screen.blit(txt_surface, (10, WINDOW_HEIGHT - 30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            # Select tile type by number keys
            if event.key == pygame.K_1: current_tile = TILES['Wall']
            elif event.key == pygame.K_2: current_tile = TILES['Blue']
            elif event.key == pygame.K_3: current_tile = TILES['Red']
            elif event.key == pygame.K_4: current_tile = TILES['Goal']
            elif event.key == pygame.K_5: current_tile = TILES['Spike']
            elif event.key == pygame.K_6: current_tile = TILES['Player']
            elif event.key == pygame.K_0: current_tile = TILES['Empty']
            elif event.key == pygame.K_s:  # Save/export
                export_level()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx = mx // TILE_SIZE
            gy = my // TILE_SIZE
            if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                if event.button == 1:  # Left click = place tile
                    if current_tile == 'P':
                        # Only allow 1 player
                        for y in range(GRID_HEIGHT):
                            for x in range(GRID_WIDTH):
                                if grid[y][x] == 'P':
                                    grid[y][x] = '0'
                    grid[gy][gx] = current_tile
                elif event.button == 3:  # Right click = delete tile
                    grid[gy][gx] = '0'
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
