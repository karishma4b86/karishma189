import pygame
import random
pygame.init()

WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Car Racing with Pause")

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  

CAR_WIDTH, CAR_HEIGHT = 50, 90
player = pygame.Rect(WIDTH//2 - CAR_WIDTH//2, HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)

class Obstacle:
    def __init__(self):
        self.width = random.randint(40, 70)
        self.height = random.randint(70, 120)
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = 5
    
    def move(self):
        self.y += self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
    
    def off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bonus:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = 5
    
    def move(self):
        self.y += self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.size, self.size))
    
    def off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

line_width = 10
line_height = 40
line_gap = 30
lines = []
for i in range(20):
    x = WIDTH//2 - line_width//2
    y = i * (line_height + line_gap)
    lines.append(pygame.Rect(x, y, line_width, line_height))

line_speed = 10
clock = pygame.time.Clock()
FPS = 60

obstacles = []
spawn_timer = 0
spawn_interval = 1500 

bonus_items = []
bonus_spawn_timer = 0
bonus_spawn_interval = 4000 

speed_increase_timer = 0
speed_increase_interval = 5000 
obstacle_speed = 5

score = 0
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)

running = True
game_over = False
paused = False
game_started = False 


button_width, button_height = 200, 80
button_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - button_height//2, button_width, button_height)

while running:
    dt = clock.tick(FPS)
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_started = True
            elif event.type == pygame.KEYDOWN:
                game_started = True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if not game_over:
                        paused = not paused

    if not game_started:
       
        title_text = large_font.render("Car Racing", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))

        pygame.draw.rect(screen, YELLOW, button_rect)
        play_text = font.render("PLAY NOW", True, GRAY)
        screen.blit(play_text, (button_rect.centerx - play_text.get_width()//2, button_rect.centery - play_text.get_height()//2))

    else:
        if not game_over and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= 8
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += 8
            for line in lines:
                line.y += line_speed
                if line.y > HEIGHT:
                    line.y = -line_height - line_gap
                pygame.draw.rect(screen, YELLOW, line)
            
            # Spawn obstacles
            spawn_timer += dt
            if spawn_timer > spawn_interval:
                spawn_timer = 0
                obs = Obstacle()
                obs.speed = obstacle_speed
                obstacles.append(obs)

            # Spawn bonus items
            bonus_spawn_timer += dt
            if bonus_spawn_timer > bonus_spawn_interval:
                bonus_spawn_timer = 0
                bonus = Bonus()
                bonus.speed = obstacle_speed
                bonus_items.append(bonus)

            # Move and draw obstacles
            for obs in obstacles[:]:
                obs.move()
                obs.draw(screen)
                if obs.off_screen():
                    obstacles.remove(obs)
                    score += 1
                if player.colliderect(obs.get_rect()):
                    game_over = True

            for bonus in bonus_items[:]:
                bonus.move()
                bonus.draw(screen)
                if bonus.off_screen():
                    bonus_items.remove(bonus)
                elif player.colliderect(bonus.get_rect()):
                    score += 5 
                    bonus_items.remove(bonus)

            speed_increase_timer += dt
            if speed_increase_timer > speed_increase_interval:
                speed_increase_timer = 0
                obstacle_speed += 1
                line_speed += 1
                if spawn_interval > 500:
                    spawn_interval -= 100
                if bonus_spawn_interval > 1000:
                    bonus_spawn_interval -= 100 

            pygame.draw.rect(screen, WHITE, player)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        elif paused:
            pause_text = font.render("PAUSED - Press P to Resume", True, WHITE)
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 20))
            for line in lines:
                pygame.draw.rect(screen, YELLOW, line)
            for obs in obstacles:
                obs.draw(screen)
            for bonus in bonus_items:
                bonus.draw(screen)
            pygame.draw.rect(screen, WHITE, player)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        else:
            over_text = font.render("GAME OVER! Press R to Restart or Q to Quit", True, WHITE)
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 20))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                obstacles.clear()
                bonus_items.clear()
                player.x = WIDTH//2 - CAR_WIDTH//2
                obstacle_speed = 5
                line_speed = 10
                spawn_interval = 1500
                bonus_spawn_interval = 4000
                score = 0
                game_over = False
                paused = False
            if keys[pygame.K_q]:
                running = False

    pygame.display.flip()

pygame.quit()
