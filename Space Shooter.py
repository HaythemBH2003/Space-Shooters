import pygame
pygame.init()

MIXER = pygame.mixer
MIXER.init()

W, H = 900, 500
SHIP_W, SHIP_H = 55, 40

GRAY = (160, 160, 160)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

WINNER_FONT = pygame.font.Font("freesansbold.ttf", 100)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)

FPS = 60
SHIP_SPEED = 5
BULLET_SPEED = 7
SHOTS_ALLOWED = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

WINDOW = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Shooters")

SPACE = pygame.transform.scale(pygame.image.load("Assets\space.png"), (W, H))
SPACESHIP_RED = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Assets\spaceship_red.png"), (SHIP_W, SHIP_H)), 270)
SPACESHIP_YELLOW = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Assets\spaceship_yellow.png"), (SHIP_W, SHIP_H)), 90)
GUN = MIXER.music.load("Assets\Assets_Gun+Silencer.mp3")

def draw(red, yellow, red_bullets, yellow_bullets, winner, yellow_health, red_health, game_over):
    WINDOW.blit(SPACE, (0, 0))
    WINDOW.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))
    WINDOW.blit(SPACESHIP_RED, (red.x, red.y))
    pygame.draw.rect(WINDOW, GRAY, (W // 2 - 5, 5, 10, H - 10))

    for bullet in red_bullets:
        if not game_over:
            pygame.draw.rect(WINDOW, RED, bullet)
    for bullet in yellow_bullets:
        if not game_over:
            pygame.draw.rect(WINDOW, YELLOW, bullet)

    if winner != "":
        if winner == "YELLOW WON !":
            text = WINNER_FONT.render(winner, True, YELLOW)
        elif winner == "RED WON !":
            text = WINNER_FONT.render(winner, True, RED)
        RECT = text.get_rect()
        RECT.centerx, RECT.centery = W // 2, H // 2 - 100
        WINDOW.blit(text, RECT)
        RESTART_TEXT = HEALTH_FONT.render("PRESS SPACE TO RESTART !", True, WHITE)
        RESTART_TEXT_RECT = RESTART_TEXT.get_rect()
        RESTART_TEXT_RECT.centerx, RESTART_TEXT_RECT.centery = W // 2, H - 75
        WINDOW.blit(RESTART_TEXT, RESTART_TEXT_RECT)
    
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", True, YELLOW)
    YELLOW_HEALTH_RECT = yellow_health_text.get_rect()
    YELLOW_HEALTH_RECT.centerx, YELLOW_HEALTH_RECT.centery = 80, 50
    WINDOW.blit(yellow_health_text, YELLOW_HEALTH_RECT)
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", True, RED)
    RED_HEALTH_RECT = red_health_text.get_rect()
    RED_HEALTH_RECT.centerx, RED_HEALTH_RECT.centery = W - 80, 50
    WINDOW.blit(red_health_text, RED_HEALTH_RECT)

    pygame.display.update()

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP]:
        if red.y > SHIP_W:
            red.y -= SHIP_SPEED
    if keys_pressed[pygame.K_DOWN]:
        if red.y < H - 2*SHIP_W:
            red.y += SHIP_SPEED
    if keys_pressed[pygame.K_RIGHT]:
        if red.x < W - 2 * SHIP_H:
            red.x += SHIP_SPEED
    if keys_pressed[pygame.K_LEFT]:
        if red.x > W // 2 + SHIP_H:
            red.x -= SHIP_SPEED

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_z]:
        if yellow.y > SHIP_W:    
            yellow.y -= SHIP_SPEED
    if keys_pressed[pygame.K_s]:
        if yellow.y < H - 2*SHIP_W:
            yellow.y += SHIP_SPEED
    if keys_pressed[pygame.K_d]:
        if yellow.x < W // 2 - 2*SHIP_H:
            yellow.x += SHIP_SPEED
    if keys_pressed[pygame.K_q]:
        if yellow.x > SHIP_H:
            yellow.x -= SHIP_SPEED

def move_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x > W:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)

def mainloop():
    red = pygame.Rect(W - W // 4, H //2, SHIP_W, SHIP_H)
    yellow = pygame.Rect(W // 4, H // 2, SHIP_W, SHIP_H)

    run = True
    game_over = False
    clock = pygame.time.Clock()

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    winner = ""

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < SHOTS_ALLOWED:
                    yellow_bullets.append(pygame.Rect(yellow.x + SHIP_H, yellow.y + SHIP_W // 2, 10, 5))
                if event.key == pygame.K_RCTRL and len(red_bullets) < SHOTS_ALLOWED:  
                    red_bullets.append(pygame.Rect(red.x - SHIP_H, red.y + SHIP_W // 2, 10, 5))
            if event.type == RED_HIT and not game_over:
                red_health -= 1
                if red_health == 0:
                    game_over = True
                    winner = "YELLOW WON !"
            if event.type == YELLOW_HIT and not game_over:
                yellow_health -= 1
                if yellow_health == 0:
                    game_over = True
                    winner = "RED WON !"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        red_health, yellow_health = 10, 10
                        game_over = False
                        winner = ""
                        red_bullets, yellow_bullets = [], []
        
        pygame.display.update()
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        yellow_movement(keys_pressed, yellow)

        move_bullets(yellow_bullets, red_bullets, yellow, red)

        draw(red, yellow, red_bullets, yellow_bullets, winner, yellow_health, red_health, game_over)


    pygame.quit()

mainloop()