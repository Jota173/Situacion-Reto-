import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#ventana
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOTTOM_PANEL

# Configura la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG")

# Variables del juego
current_fighter = 1  
total_fighters = 5 
action_cooldown = 0
wait_time = 60  
attack = False
potion = False
potion_effect = 15  
clicked = False
game_over = 0

# Cargar fuentes y colores
font = pygame.font.SysFont('Times New Roman', 20)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Cargar imágenes
background_img = pygame.image.load("image/rpgdg.png").convert_alpha()
panel_img = pygame.image.load("image/panel.png").convert_alpha()
potion_img = pygame.image.load("image/potion.png").convert_alpha()
restart_img = pygame.image.load("image/restart.png").convert_alpha()
victory_img = pygame.image.load("image/victory.png").convert_alpha()
lose_img = pygame.image.load("image/gameover.png").convert_alpha()
sword_img = pygame.image.load("image/sword.png").convert_alpha()


#dibujar texto en la pantalla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#dibujar el fondo
def draw_bg():
    screen.blit(background_img, (0, 0))

#dibujar el panel
def draw_panel():
    screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))
    draw_text(f"{Claude.name} HP: {Claude.hp}", font, white, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10)
    draw_text(f"{Agumon.name} HP: {Agumon.hp}", font, white, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 55)
    draw_text(f"{Link.name} HP: {Link.hp}", font, white, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 100)
    for count, i in enumerate(bandit_list):
        draw_text(f'{i.name} HP: {i.hp}', font, white, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60)

#Clase de personaje
class Character():
    def __init__(self, x, y, name, max_hp, strength, potions, image_path, scale):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(image_path)
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)

    def use_potion(self):
        if self.potions > 0 and self.hp < self.max_hp:
            heal_amount = potion_effect
            if self.hp + heal_amount > self.max_hp:
                heal_amount = self.max_hp - self.hp
            self.hp += heal_amount
            self.potions -= 1
            heal_text = DamageText(self.rect.centerx, self.rect.y, str(heal_amount), green)
            damage_text_group.add(heal_text)

    def draw(self):
        screen.blit(self.image, self.rect)

class Healthbar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, int(150 * ratio), 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        
    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()

# Inicializa personajes
Claude = Character(300, 280, "Claude", 100, 15, 3, "image/claude.png", 0.125)
Agumon = Character(190, 280, "Agumon", 100, 25, 3, "image/agumon.gif", 0.4)
Link = Character(100, 280, "Link", 100, 20, 3, "image/link.gif", 0.5)

bandit1 = Character(550, 270, 'Bandit1', 90, 15, 2, "image/bandit.png", 1)
bandit2 = Character(700, 270, 'Bandit2', 90, 15, 2, "image/bandit.png", 1)

bandit_list = [bandit1, bandit2]

# Crea barras de salud para personajes
Claude_Health_Bar = Healthbar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 35, Claude.hp, Claude.max_hp)
Agumon_Health_Bar = Healthbar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 80, Agumon.hp, Agumon.max_hp)
Link_Health_Bar = Healthbar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 120, Link.hp, Link.max_hp)
bandit1_health_bar = Healthbar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = Healthbar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 100, bandit2.hp, bandit2.max_hp)

potion_button1 = button.Button(screen, 250, SCREEN_HEIGHT - BOTTOM_PANEL + 5, potion_img, 64, 64)
potion_button2 = button.Button(screen, 250, SCREEN_HEIGHT - BOTTOM_PANEL + 50, potion_img, 64, 64)
potion_button3 = button.Button(screen, 250, SCREEN_HEIGHT - BOTTOM_PANEL + 95, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:
    clock.tick(fps)
    draw_bg()
    draw_panel()

    # Dibuja barras de salud
    Claude_Health_Bar.draw(Claude.hp)
    Agumon_Health_Bar.draw(Agumon.hp)
    Link_Health_Bar.draw(Link.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    Claude.draw()
    Agumon.draw()
    Link.draw()
    for bandit in bandit_list:
        bandit.draw()

    damage_text_group.update()
    damage_text_group.draw(screen)

    attack = False
    target = None
    clicked = False 
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()

    # seleccionar a quien atacar
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos) and bandit.alive:
            pygame.mouse.set_visible(False)
            screen.blit(sword_img, pos)
            if pygame.mouse.get_pressed()[0] == 1 and not clicked:
                attack = True
                target = bandit
                clicked = True

    #pociones
    if potion_button1.draw():
        if Claude.alive and Claude.potions > 0:
            Claude.use_potion()
    draw_text(str(Claude.potions), font, white, 260, SCREEN_HEIGHT - BOTTOM_PANEL + 5)
    
    if potion_button2.draw():
        if Agumon.alive and Agumon.potions > 0:
            Agumon.use_potion()
    draw_text(str(Agumon.potions), font, white, 260, SCREEN_HEIGHT - BOTTOM_PANEL + 50)
    
    if potion_button3.draw():
        if Link.alive and Link.potions > 0:
            Link.use_potion()
    draw_text(str(Link.potions), font, white, 260, SCREEN_HEIGHT - BOTTOM_PANEL + 95)

    if game_over == 0:
        if Claude.alive:
            if current_fighter == 1:
                if action_cooldown >= wait_time:
                    if attack and target:
                        Claude.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
        if Agumon.alive:
            if current_fighter == 2:
                if action_cooldown >= wait_time:
                    if attack and target:
                        Agumon.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
        if Link.alive:
            if current_fighter == 3:
                if action_cooldown >= wait_time:
                    if attack and target:
                        Link.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 4 + count:
                if bandit.alive:
                    if action_cooldown >= wait_time:
                        bandit.attack(random.choice([Claude, Agumon, Link]))
                        current_fighter += 1
                        action_cooldown = 0
                else:
                    current_fighter += 1
        if current_fighter > total_fighters:
            current_fighter = 1
        action_cooldown += 1
    else:
        game_over = -1
    
    # Verificar si todos los bandidos han muerto
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1

    
    if game_over == 1:
        screen.blit(victory_img, (250, 50))  
    elif game_over == -1:
        screen.blit(lose_img, (250, 50)) 

    
    if game_over != 0 and restart_button.draw():
        Claude = Character(300, 280, "Claude", 100, 15, 3, "image/claude.png", 0.125)
        Agumon = Character(190, 280, "Agumon", 100, 25, 3, "image/agumon.gif", 0.4)
        Link = Character(100, 280, "Link", 100, 20, 3, "image/link.gif", 0.5)

        bandit1 = Character(550, 270, 'Bandit1', 90, 15, 2, "image/bandit.png", 1)
        bandit2 = Character(700, 270, 'Bandit2', 90, 15, 2, "image/bandit.png", 1)

        
        bandit_list = [bandit1, bandit2]
        current_fighter = 1
        action_cooldown = 0
        game_over = 0

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

