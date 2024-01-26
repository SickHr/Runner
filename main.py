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


# Load background
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Load snail animations
snail1_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail2_surface = pygame.image.load("graphics/snail/snail2.png").convert_alpha()

snail_animations = [snail1_surface, snail2_surface]
snail_animation_index = 0
snail_surface = snail_animations[snail_animation_index]

snail_rect = snail_surface.get_rect(midbottom=(600, 300))

# Load player animations
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_animations = [player_stand, player_walk1, player_walk2, player_jump]
player_animation_index = 0
player_surface = player_animations[player_animation_index]

player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0
is_jumping = False

# Score
score_surface = game_font.render("Score: 0", False, "Black")
score_rect = score_surface.get_rect(center=(70, 30))
score = 0

# Game states
game_active = True
game_over = False

# Animation timers
player_animation_timer = pygame.time.get_ticks()
snail_animation_timer = pygame.time.get_ticks()

# Game loop
while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300 and not game_over:
                player_gravity = -12
                is_jumping = True

    if not game_over:
        # Collision
        if player_rect.colliderect(snail_rect):
            game_over = True

        # Update game elements
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = WIDTH
            score += 1  # Increase score when snail reaches the left side

        # Player animation update
        current_time = pygame.time.get_ticks()
        if is_jumping:
            player_animation_index = 3  # Use the jump animation while jumping
            is_jumping = False
        elif current_time - player_animation_timer > 200:  # Change the frame every 200 milliseconds
            player_animation_timer = current_time
            player_animation_index = (player_animation_index + 1) % (len(player_animations) - 1)  # Exclude jump animation

        player_surface = player_animations[player_animation_index]

        # Snail animation update
        if current_time - snail_animation_timer > 300:  # Change the frame every 300 milliseconds
            snail_animation_timer = current_time
            snail_animation_index = (snail_animation_index + 1) % len(snail_animations)
            snail_surface = snail_animations[snail_animation_index]

        # Player
        player_gravity += 0.5
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

    # Draw elements
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))

    screen.blit(player_surface, player_rect)
    screen.blit(snail_surface, snail_rect)

    # Update and display score
    score_surface = game_font.render(f"Score: {score}", False, "Black")
    screen.blit(score_surface, score_rect)

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
        score = 0  # Reset the score
