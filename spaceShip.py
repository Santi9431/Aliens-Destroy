import pygame, random
import sys

# Define las constantes y el tamaño de tu ventana 
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicializa Pygame
pygame.font.init()  # Inicializa la biblioteca de fuentes
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú de Juego")
clock = pygame.time.Clock()
pygame.font.init()
# Inicialmente, el juego comienza en el menú 
game_state = "menu"  


# ponemos esta funcion global por que me permite mostrar 
def draw_text(surface, text, size, x, y):
        font = pygame.font.SysFont("serif", size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

# Función para crear botones
def create_button(surface, text, x, y, width, height, text_size, bg_color, text_color, action):
    button_font = pygame.font.Font(None, text_size)
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + (width / 2), y + (height / 2))
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    surface.blit(text_surface, text_rect)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        if click[0] == 1:
            if action == "start":
                start_game()
            elif action == "instructions":
                show_instructions()

# Función para iniciar el juego
def start_game():

    global game_over, score, game_state    # Declarar score como global
    
    game_over = False
    score = 0  # Inicializar la variable score
    WIDTH = 800
    HEIGHT = 600
    BLACK = (0, 0, 0)
    WHITE = ( 255, 255, 255)
    GREEN = (0, 255, 0)

    
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aliens Destroy")
    clock = pygame.time.Clock()

    
    def draw_shield_bar(surface, x, y, percentage):
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = (percentage / 100) * BAR_LENGHT
        border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, GREEN, fill)
        pygame.draw.rect(surface, WHITE, border, 2)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.original_image = pygame.image.load("recursos/player.png").convert()
            self.original_image.set_colorkey(BLACK)
            self.image = self.original_image.copy()
            self.large_image = pygame.image.load("recursos/player5_sinfondo.png").convert()  # Nueva imagen
            self.large_image.set_colorkey(BLACK)  # Opcional, si necesitas configurar el color clave
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10
            self.speed_x = 0
            self.shield = 100
            self.lasers = 1  # Inicialmente, el jugador puede disparar un solo láser

        def update(self):
            global score  # Declarar score como global
            self.speed_x = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speed_x = -5
            if keystate[pygame.K_RIGHT]:
                self.speed_x = 5
            self.rect.x += self.speed_x
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

            # Cambiar la imagen de la nave si el jugador tiene más de 200 puntos
            if score > 200:
                self.image = pygame.transform.scale(self.large_image, (100, 50))
                self.image.set_colorkey(BLACK)

        def shoot(self):
            if score > 200:
                bullet1 = Bullet(self.rect.centerx - 10, self.rect.top)  # Primer láser
                bullet2 = Bullet(self.rect.centerx + 10, self.rect.top)  # Segundo láser
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
            else:
                bullet = Bullet(self.rect.centerx, self.rect.top)  # Un solo láser
                all_sprites.add(bullet)
                bullets.add(bullet)
            laser_sound.play()


    class Meteor(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = random.choice(meteor_images)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)
            self.speedx = random.randrange(-5, 5)

        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-140, - 100)
                self.speedy = random.randrange(1, 10)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.image.load("recursos/laser1.png")
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center):
            super().__init__()
            self.image = explosion_anim[0]
            self.rect = self.image.get_rect()
            self.rect.center = center 
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(explosion_anim):
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = explosion_anim[self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center


    def show_go_screen():
        screen.blit(background, [0,0])
        draw_text(screen, "Aliens Destroy", 65, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, "Creado por Santiago Espinosa Otálvaro", 15, WIDTH // 2, HEIGHT * 1/8 )
        draw_text(screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3/4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False


    meteor_images = []
    meteor_list = ["recursos/meteorGrey_big1.png", "recursos/meteorGrey_big2.png", "recursos/meteorGrey_big3.png", "recursos/meteorGrey_big4.png",
                    "recursos/meteorGrey_med1.png", "recursos/meteorGrey_med2.png", "recursos/meteorGrey_small1.png", "recursos/meteorGrey_small2.png",
                    "recursos/meteorGrey_tiny1.png", "recursos/meteorGrey_tiny2.png"]
    for img in meteor_list:
        meteor_images.append(pygame.image.load(img).convert())


    ####----------------EXPLOSTION IMAGENES --------------
    explosion_anim = []
    for i in range(9):
        file = "recursos/regularExplosion0{}.png".format(i)
        img = pygame.image.load(file).convert()
        img.set_colorkey(BLACK)
        img_scale = pygame.transform.scale(img, (70,70))
        explosion_anim.append(img_scale)

    # Cargar imagen de fondo
    background = pygame.image.load("recursos/background.png").convert()

    # Cargar sonidos
    laser_sound = pygame.mixer.Sound("recursos/laser5.ogg")
    explosion_sound = pygame.mixer.Sound("recursos/explosion.wav")
    pygame.mixer.music.load("recursos/music.ogg")
    pygame.mixer.music.set_volume(0.2)

    # Aca genero el sonido de fondo en el menu 
    pygame.mixer.music.play(loops=-1)

    #### ----------GAME OVER
    game_over = True
    running = True
    while running:
        if game_over:
            show_go_screen()

            game_over = False
            game_state = "menu" 
            all_sprites = pygame.sprite.Group()
            meteor_list = pygame.sprite.Group()
            bullets = pygame.sprite.Group()

            player = Player()
            all_sprites.add(player)
            for i in range(8):
                meteor = Meteor()
                all_sprites.add(meteor)
                meteor_list.add(meteor)
            score = 0
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

            if player.shield <= 0 and not game_over:
                game_state = "menu"
                game_over = True  # Establecer game_over en True para evitar que se inicie el juego nuevamente


        all_sprites.update()

        #colisiones - meteoro - laser
        hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
        for hit in hits:
            score += 10
            explosion_sound.play()
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        # Checar colisiones - jugador - meteoro
        hits = pygame.sprite.spritecollide(player, meteor_list, True)
        for hit in hits:
            player.shield -= 25
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)
            if player.shield <= 0:
                game_over = True

        screen.blit(background, [0, 0])

        all_sprites.draw(screen)

        #Marcador
        draw_text(screen, str(score), 25, WIDTH // 2, 10)

        # Escudo.
        draw_shield_bar(screen, 5, 5, player.shield)

        pygame.display.flip()
    pygame.quit()
# Funcion para mostrar las instrucciones
def show_instructions():

    instructions = [
        "Instrucciones:",
        "1. Usa las flechas izquierda y derecha para mover la nave.",
        "2. Presiona la barra espaciadora para disparar.",
        "3. Evita los asteroides para sobrevivir.",
        "4. Gana puntos al destruir asteroides.",
        "5. Presiona X para regresar al menu",
        "6. ¡Diviértete!",
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)  # Limpia la pantalla

        # Muestra las instrucciones en la ventana
        y = 100
        for line in instructions:
            draw_text(screen, line, 24, WIDTH // 2, y)
            y += 30

        pygame.display.flip()
# Funcion para regresar al menu
# def show_menu():
#     menu_running = True
#     while menu_running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         # Cargar imagen de fondo para el menú
#         menu_background = pygame.image.load("recursos/space.jpeg").convert()
#         screen.blit(menu_background, (0, 0))  # Sin cambios en la posición
#         menu_background = pygame.image.load("recursos/space.jpeg").convert()
#         menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
#         create_button(screen, "Continuar", 300, 200, 200, 50, 36, WHITE, BLACK, "continue")
#         create_button(screen, "Instrucciones", 300, 300, 200, 50, 24, WHITE, BLACK, "instructions")
#         create_button(screen, "Regresar al Menú", 300, 400, 200, 50, 24, WHITE, BLACK, "return_to_menu")

#         pygame.display.update()
#         clock.tick(60)

# Cargar imagen de fondo para el menú
menu_background = pygame.image.load("recursos/space.jpeg").convert()

# ... Código previo ...

# Bucle principal
menu_running = True
game_over = False
game_state = "menu"  # Inicialmente, el juego comienza en el menú

while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(menu_background, (0, 0))
    menu_background = pygame.image.load("recursos/space.jpeg").convert()
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

    if game_state == "menu":
        create_button(screen, "Start!", 300, 200, 200, 50, 36, WHITE, BLACK, "start")
        create_button(screen, "Instrucciones", 300, 300, 200, 50, 24, WHITE, BLACK, "instructions")
    elif game_state == "playing":
        start_game()  # Inicia el juego
        game_state = "menu"  # Después de terminar el juego, vuelve al menú

    pygame.display.update()
    clock.tick(60)

