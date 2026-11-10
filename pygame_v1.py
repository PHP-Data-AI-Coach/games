import pygame
import sys
import random
import array
import math  # 🛠️ FIXED: Added the standard Python math library

# 1. Initialize Pygame and setup the window canvas
pygame.init()
pygame.mixer.init() 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge & Win!")

clock = pygame.time.Clock()
pygame.font.init()
game_font = pygame.font.SysFont("Arial", 30)
victory_font = pygame.font.SysFont("Arial", 50, bold=True)

# --- 🔊 FIXED SOUND GENERATOR ---
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = array.array('h', [0] * n_samples)
    
    for i in range(n_samples):
        t = float(i) / sample_rate
        # 🛠️ FIXED: Changed pygame.math.sin to math.sin
        raw_sine = math.sin(2.0 * math.pi * frequency * t)
        
        # 🛠️ FIXED: Replaced pygame.math.clamp with a universal version check layout
        clamped_sine = max(-1.0, min(1.0, raw_sine))
        buf[i] = int(32767.0 * 0.5 * clamped_sine)
        
    sound_bytes = array.array('h')
    for sample in buf:
        sound_bytes.append(sample)
        sound_bytes.append(sample)
    return pygame.mixer.Sound(buffer=sound_bytes)

# Create our audio effects
point_sound = generate_beep_sound(frequency=600, duration=0.15) 
game_over_sound = generate_beep_sound(frequency=150, duration=0.4) 

# --- GAME VARIABLES ---
score = 0
WINNING_SCORE = 10  # ⭐ FEATURE 2: WIN CONDITION TARGET
game_state = "PLAYING" # Can be "PLAYING", "VICTORY", or "GAME_OVER"

# Player Attributes
player_width, player_height = 50, 50
player_x = (SCREEN_WIDTH // 2) - (player_width // 2)
player_y = SCREEN_HEIGHT - 100
player_speed = 7

# Jump Variables
is_jumping = False
jump_count = 10

# Obstacle Attributes
obstacle_width, obstacle_height = 50, 50
obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
obstacle_y = -50
obstacle_speed = 5

# --- CORE GAME LOOP ---
while True:
    # 2. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # If the game is finished, allow them to press ENTER to restart
        if game_state != "PLAYING" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                score = 0
                obstacle_speed = 5
                obstacle_y = -50
                player_x = (SCREEN_WIDTH // 2) - (player_width // 2)
                game_state = "PLAYING"

    # 3. Game Logic updates depending on State
    if game_state == "PLAYING":
        keys = pygame.key.get_pressed()
        
        # Horizontal Movement
        if keys[pygame.K_LEFT]: player_x -= player_speed
        if keys[pygame.K_RIGHT]: player_x += player_speed

        # Jump Logic
        if not is_jumping:
            if keys[pygame.K_SPACE]: is_jumping = True
        else:
            if jump_count >= -10:
                neg = 1 if jump_count >= 0 else -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Boundary Restraints
        if player_x < 0: player_x = 0
        if player_x > SCREEN_WIDTH - player_width: player_x = SCREEN_WIDTH - player_width

        # Obstacle Movement
        obstacle_y += obstacle_speed

        # Score / Reset Obstacle
        if obstacle_y > SCREEN_HEIGHT:
            obstacle_y = -50
            obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
            score += 1
            obstacle_speed += 0.5
            
            # 🔊 FEATURE 1: Play scoring sound effect
            point_sound.play()
            
            # ⭐ FEATURE 2: Check for Win Condition
            if score >= WINNING_SCORE:
                game_state = "VICTORY"

        # Collision System
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        if player_rect.colliderect(obstacle_rect):
            game_over_sound.play() # 🔊 Play crash sound effect
            game_state = "GAME_OVER"

    # 4. Rendering Engine
    screen.fill((0, 0, 0)) # Wipe screen black

    if game_state == "PLAYING":
        # Draw game elements
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
        pygame.draw.rect(screen, (0, 0, 255), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
        
        # UI Score
        score_surface = game_font.render(f"Score: {score} / {WINNING_SCORE}", True, (255, 255, 255))
        screen.blit(score_surface, (20, 20))

    elif game_state == "VICTORY":
        # ⭐ Draw Victory Screen
        vic_surface = victory_font.render("YOU WIN! 🏆", True, (0, 255, 0))
        retry_surface = game_font.render("Press ENTER to play again", True, (255, 255, 255))
        screen.blit(vic_surface, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50))
        screen.blit(retry_surface, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 20))

    elif game_state == "GAME_OVER":
        # Draw Game Over Screen
        lose_surface = victory_font.render("GAME OVER ❌", True, (255, 0, 0))
        retry_surface = game_font.render("Press ENTER to try again", True, (255, 255, 255))
        screen.blit(lose_surface, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 50))
        screen.blit(retry_surface, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(60)
	