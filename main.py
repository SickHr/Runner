import pygame

pygame.init()

# Create the screen
WIDTH = 800
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

# Load font
game_font = pygame.font.Font("font/Pixeltype.ttf", 45)

font_surface = game_font.render("Runner ", False, "Black")
font_rect = font_surface.get_rect(center=(400, 50))

# Load background
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Load snail
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

# Load player
surface_player = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = surface_player.get_rect(midbottom=(80, 300))
player_gravity = 0

# Game states
game_active = True
game_over = False

# Game loop
while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300 and not game_over:
                player_gravity = -12

    if not game_over:
        # Collision
        if player_rect.colliderect(snail_rect):
            game_over = True

        # Update game elements
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = WIDTH

        # Player
        player_gravity += 0.5
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

    # Draw elements
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen, "#c0e8ec", font_rect)
    screen.blit(font_surface, font_rect)
    screen.blit(surface_player, player_rect)
    screen.blit(snail_surface, snail_rect)

    if game_over:
        # Game over screen
        game_over_surface = game_font.render("Game Over", True, "Black")
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.update()
    clock.tick(60)

    # Restart the game if space is pressed after game over
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and game_over:
        game_over = False
        player_rect.midbottom = (80, 300)
        snail_rect.midbottom = (WIDTH, 300)
        player_gravity = 0

pygame.quit()
exit()
