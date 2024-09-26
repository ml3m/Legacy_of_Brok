import pygame
import random
import math
import sys
from enum import Enum
from user_settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    START_MAX_HP,
    START_MAX_XP,
    DAMAGE_COOLDOWN,
    PLAYER_COL_RADIUS,
    SHOOT_DELAY,
    BULLET_SPEED,
    PLAYER_SPEED,
    ENEMY_COL_RADIUS,
    ENEMY_SPAWN_RATE,
    FPS,
)

from load import (
    player_image,
    reset_image,
    background_image,
    shot_effect,
    gun_image,
    gun_image_rev,
    projectile_image,
    enemy_images,
    drop_image,
    magma_projectile_img,
    magma_ball,
)

enemies = []
active_items = []

BULLET_SPEED_2 = 200
BULLET_SPEED_1 = 300

class Game:
    def __init__(self):
        self.initialize_pygame()    #call fun
        self.setup_game()           #call fun
        self.setup_player()         #call fun

    def initialize_pygame(self):
        pygame.init()   #initialize all imported pygame modules
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))    #creating a screen instance
        pygame.display.set_caption("Legacy of Brok")    #window title init 
        pygame.display.set_icon(player_image)   #window icon init
        self.font = pygame.font.Font(None, 64)  #font init
        self.clock = pygame.time.Clock()    #clock time init

    def setup_game(self):
        self.running = True     #game running boolean init
        self.game_over = False  #game_over running boolean init
        self.dt = 0     #Delta time init
        self.xp_bar = XPBar(max_xp=START_MAX_XP)    #bar init obj
        self.hp_bar = HPBar(max_hp=START_MAX_HP)    #bar init obj
        self.last_damage_time = 0   
        """  last_damage_time  --- is used to store the time (in milliseconds since the start of the Pygame application) when the player was last damaged. This information is used to implement a cooldown for damage, preventing the player from taking damage too frequently within a specified cooldown period."""
        self.reset_button_rect = reset_image.get_rect()     #stores the reset img rect
        self.reset_button_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100)     #stores a tuple of the position of center for reset button

    def setup_player(self):
        self.player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), xp_bar=self.xp_bar)    #creates a instance of Player obj

    def reset_game(self):
        self.game_over = False      #resets the game_over to False, when game is stopped the var is turned to True
        self.reset_player()         #call fun
        self.reset_enemies()        #call fun
        self.reset_items()          #call fun

    def reset_player(self):
        self.player.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)  #resets the player to the centre of the screen
        self.player.collected_items = []    #resets the colelcted_items 
        self.player.level = 1       #resets the player level to 1
        self.player.xp = 0          #resets the player xp to 1

    def reset_enemies(self):
        Enemy.enemies.clear()   #clears all the enemies on the screeen
        Enemy.active_explosions.clear()     #clears all the explosions on the screen

    def reset_items(self):
        active_items.clear()    #clears all the items on the screen
        self.xp_bar.current_xp = 0      #reset the xp bar
        self.xp_bar.max_xp = START_MAX_XP   #reset the max xp to the default 
        self.xp_bar.level = 1     #resets the xp bar level to 1
        self.hp_bar.current_hp = START_MAX_HP   #resets the hp bar to the starting amount of hp
        self.player.projectiles.clear()     #clears all the projectiles on the screen
    #GAME MAIN LOOP
    def run(self):
        while self.running:
            self.handle_events()
            mouse_pos = pygame.mouse.get_pos()
    
            if not self.game_over:
                self.update_game(mouse_pos)
            else:
                self.display_game_over_screen()
                self.check_reset_button()

            self.update_display_and_fps()

        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update_game(self, mouse_pos):
        self.screen.blit(background_image, (0, 0))
        keys = pygame.key.get_pressed()
        self.player.update(self.dt, keys, mouse_pos=mouse_pos)
        self.player.draw(self.screen)

        self.update_enemies()
        self.handle_bullet_enemy_collisions()
        self.handle_explosions()
        self.remove_off_screen_elements()
        self.handle_enemy_collisions()
        Enemy.spawn_random_enemy(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.update_bullets_display()
        self.update_enemies_display()
        self.update_active_items_display()
        self.draw_bars()
    
    def update_enemies(self):
        for enemy in Enemy.enemies[:]:
            enemy.update(self.dt, self.player)

            # Update and draw enemy bullets
            for bullet in enemy.projectiles[:]:
                bullet.update(self.dt)
                rotated_bullet = pygame.transform.rotate(bullet.image, -bullet.angle)
                rotated_rect = rotated_bullet.get_rect(center=bullet.rect.center)
                self.screen.blit(rotated_bullet, rotated_rect.topleft)
    
    def handle_bullet_enemy_collisions(self):
        for bullet in self.player.projectiles[:]:
            bullet.update(self.dt)
            for enemy in Enemy.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.handle_bullet_enemy_collision(bullet, enemy)
                    break
                
    def handle_bullet_enemy_collision(self, bullet, enemy):
        self.player.projectiles.remove(bullet)
        Enemy.enemies.remove(enemy)
        enemy.kill()
        explosion = Explosion(shot_effect, enemy.rect.center, 200)
        Enemy.active_explosions.append(explosion)
    
    def handle_explosions(self):
        for explosion in Enemy.active_explosions[:]:
            if explosion.update():
                Enemy.active_explosions.remove(explosion)
            else:
                explosion.draw(self.screen)
    
    def remove_off_screen_elements(self):
        for bullet in self.player.projectiles[:]:
            if (
                bullet.rect.left > self.screen.get_width()
                or bullet.rect.right < 0
                or bullet.rect.top > self.screen.get_height()
                or bullet.rect.bottom < 0
            ):
                self.player.projectiles.remove(bullet)
    
    def handle_enemy_collisions(self):
        for enemy in Enemy.enemies[:]:
            if enemy.check_collision(self.player):
                self.handle_player_enemy_collision(enemy)
                break
            
    def handle_player_enemy_collision(self, enemy): #not sure what enemy arg does here.
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time > DAMAGE_COOLDOWN:
            self.hp_bar.update(10)
            self.last_damage_time = current_time
            if self.hp_bar.current_hp <= 0:
                self.game_over = True
    
    def update_bullets_display(self):
        for bullet in self.player.projectiles:
            bullet.update(self.dt)
            rotated_bullet = pygame.transform.rotate(bullet.image, -bullet.angle)
            rotated_rect = rotated_bullet.get_rect(center=bullet.rect.center)
            self.screen.blit(rotated_bullet, rotated_rect.topleft)
    
    def update_enemies_display(self):
        for enemy in Enemy.enemies:
            enemy.draw(self.screen)
    
    def update_active_items_display(self):
        for item in active_items[:]:
            if isinstance(item, Crystal):
                item.draw(self.screen)
            item.draw(self.screen)
    
    def draw_bars(self):
        self.xp_bar.draw(self.screen)
        self.hp_bar.draw(self.screen)
    
    def display_game_over_screen(self):
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(reset_image, self.reset_button_rect)
    
    def check_reset_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if (
            self.reset_button_rect.collidepoint(mouse_x, mouse_y)
            and mouse_clicked[0]
        ):
            self.reset_game()
    
    def update_display_and_fps(self):
        pygame.display.flip()
        self.dt = self.clock.tick(FPS) / 1000  # limits FPS to 60

class Explosion:
    def __init__(self, image, position, duration):
        self.image = image
        self.rect = image.get_rect(center= position)
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.start_time >= self.duration

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Crystal:
    def __init__(self, image, position):
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Bullet:
    def __init__(self, image, position, velocity, angle):
        self.image = image
        self.rect = image.get_rect(center=position)
        self.velocity = velocity
        self.angle = angle

    def update(self, dt):
        self.rect.move_ip(self.velocity * dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Player:
    def __init__(self, position, xp_bar):
        self.image = player_image
        self.rect = self.image.get_rect(center=position)
        self.radius = PLAYER_COL_RADIUS
        self.gun_image = gun_image
        self.gun_rect = self.gun_image.get_rect()
        self.gun_offset = pygame.Vector2(30, 30) # player-gun relative position.
        self.gun_angle = 0
        self.projectiles = []
        self.shoot_cooldown = 0
        self.shoot_delay = SHOOT_DELAY
        self.gun_direction = pygame.Vector2(1, 0)
        self.xp = 0
        self.level = 1
        self.xp_bar = xp_bar
        self.window_bounds = pygame.display.get_surface().get_rect()

    def shoot(self, mouse_pos):
        if self.shoot_cooldown <= 0:
            direction = pygame.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
            firing_point = self.gun_rect.center 
            bullet_velocity = direction.normalize() * BULLET_SPEED
            bullet = Bullet(projectile_image, firing_point, bullet_velocity, self.gun_angle)
            self.projectiles.append(bullet)
            self.shoot_cooldown = self.shoot_delay

    def update(self, dt, keys, mouse_pos):
        if keys[pygame.K_w] and self.rect.top > self.window_bounds.top:
            self.rect.y -= PLAYER_SPEED * dt
        if keys[pygame.K_s] and self.rect.bottom < self.window_bounds.bottom:
            self.rect.y += PLAYER_SPEED * dt
        if keys[pygame.K_a] and self.rect.left > self.window_bounds.left:
            self.rect.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d] and self.rect.right < self.window_bounds.right:
            self.rect.x += PLAYER_SPEED * dt

        self.gun_rect.center = self.rect.center + self.gun_offset
        angle = math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx)
        self.gun_angle = math.degrees(angle)
        self.gun_direction = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.shoot(mouse_pos)
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        self.check_item_collision()
        
    def check_item_collision(self):
        for item in active_items[:]:
            if self.rect.colliderect(item.rect):
                active_items.remove(item)
                self.xp += 1
                self.xp_bar.update(1)  # Increment the XP bar by 1 for each collected crystal
                if self.xp_bar.current_xp == self.xp_bar.max_xp:
                    self.xp_bar.current_xp = 0
                    self.xp_bar.max_xp += 5
                    self.level += 1
                print("xp:", self.xp)  # debug console visual
                print("level: ", self.level) #debug console visual

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        rotated_gun = pygame.transform.rotate(self.gun_image, -self.gun_angle)
        
        if self.gun_angle > 90 or self.gun_angle < -90:
            self.gun_image = gun_image_rev
        else:
            self.gun_image = gun_image

        rotated_rect = rotated_gun.get_rect(center=self.gun_rect.center)
        screen.blit(rotated_gun, rotated_rect.topleft)

class Enemy:

    enemies = []
    active_explosions = []

    def __init__(self, image, spawn_point, enemy_type):
        self.image = image
        self.rect = image.get_rect(center=spawn_point)
        self.radius = ENEMY_COL_RADIUS
        self.projectiles = []
                # Adjust speed based on enemy type
        if enemy_type == EnemyType.NORMAL:
            self.speed = 100
        elif enemy_type == EnemyType.FAST:
            self.speed = 200
        elif enemy_type == EnemyType.STRONG:
            self.speed = 50
        
        self.shoot_cooldown = 0
        self.shoot_delay = 2  # Adjust the delay as needed for enemy shots

    @classmethod
    def spawn_random_enemy(cls, screen_width, screen_height):
        if random.random() < ENEMY_SPAWN_RATE:
            spawn_edge = random.choice(["top", "bottom", "left", "right"])
            if spawn_edge == "top":
                spawn_point = pygame.Vector2(random.uniform(0, screen_width), 0)
            elif spawn_edge == "bottom":
                spawn_point = pygame.Vector2(random.uniform(0, screen_width), screen_height)
            elif spawn_edge == "left":
                spawn_point = pygame.Vector2(0, random.uniform(0, screen_height))
            else:
                spawn_point = pygame.Vector2(screen_width, random.uniform(0, screen_height))

            enemy_type = random.choice([EnemyType.NORMAL, EnemyType.FAST, EnemyType.STRONG])
            enemy_image = random.choice(enemy_images)
            enemy = cls(enemy_image, spawn_point, enemy_type)
            cls.enemies.append(enemy)    

    def update(self, dt, player):
        direction = pygame.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        distance = direction.length()

        if distance > 0:
            direction.normalize_ip()
            movement = direction * min(self.speed * dt, distance)
            new_position = self.rect.center + movement
            self.rect.centerx = max(0, min(WINDOW_WIDTH, new_position[0]))
            self.rect.centery = max(0, min(WINDOW_HEIGHT, new_position[1]))

        if self.shoot_cooldown <= 0:
            self.shoot(player)
            self.shoot_cooldown = self.shoot_delay
        else:
            self.shoot_cooldown -= dt

    def shoot(self, player):

        """this is the condition of choosing which enemy will shoot a specific config of projectiles"""
        if self.image == enemy_images[2]:
            # Shoot a bullet towards the player
            direction = pygame.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
            if direction.length() > 0:
                direction.normalize_ip()
                bullet_velocity = direction * BULLET_SPEED_1  # Adjust bullet speed as needed
                bullet = Bullet(magma_projectile_img, self.rect.center, bullet_velocity, 0)  # Angle is set to 0 for simplicity
                self.projectiles.append(bullet)

        """this is the condition of choosing which enemy will shoot a specific config of projectiles"""
        if self.image == enemy_images[1]:
            # Shoot a bullet towards the player
            direction = pygame.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
            if direction.length() > 0:
                direction.normalize_ip()
                bullet_velocity = direction * BULLET_SPEED_2  # Adjust bullet speed as needed
                #image insert here: \>
                bullet = Bullet(magma_ball, self.rect.center, bullet_velocity, 0)  # Angle is set to 0 for simplicity
                self.projectiles.append(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, player):
        distance = pygame.math.Vector2(player.rect.center).distance_to(self.rect.center)
        return distance < player.radius + self.radius
        
    def kill(self):
        crytal = Crystal(drop_image, self.rect.center)
        active_items.append(crytal)

        if self in enemies:
            enemies.remove(self)    

    def drop_crystal(self):
        crystal = Crystal(self.drop_crystal, self.rect.center)
        active_items.append(crystal)

class XPBar:
    def __init__(self, max_xp):
        self.max_xp = max_xp
        self.current_xp = 0
        self.level = 1  # Initialize the level
        self.bar_color = (12, 93, 130)  # bar color
        self.bar_color2 = (24, 159, 192)  # fill color
        self.bar_rect = pygame.Rect(10, 10, 200, 20)  # Adjust the position and size as needed
        self.font = pygame.font.Font(None, 28)  # Create a font for displaying text

    def update(self, collected_xp):
        # Update the XP bar based on collected XP
        self.current_xp = min(self.max_xp, self.current_xp + collected_xp)
        if self.current_xp == self.max_xp:
            self.level += 1  # Increase the level when XP reaches max

    def draw(self, screen):
        # Draw the XP bar and level on the screen
        pygame.draw.rect(screen, self.bar_color, self.bar_rect)
        fill_width = (self.current_xp / self.max_xp) * self.bar_rect.width
        fill_rect = pygame.Rect(self.bar_rect.left, self.bar_rect.top, fill_width, self.bar_rect.height)
        pygame.draw.rect(screen, self.bar_color2, fill_rect)

        # Calculate the position of the level text on the right side of the bar
        level_text = self.font.render(f"LV.{self.level}", True, (255, 255, 255))
        text_rect = level_text.get_rect()
        text_rect.right = self.bar_rect.right - 10  # Adjust the right margin
        text_rect.centery = self.bar_rect.centery  # Center vertically

        screen.blit(level_text, text_rect)

class HPBar:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.bar_color = (255, 0, 0)  # Red bar for HP
        self.bar_rect = pygame.Rect(10, 40, 200, 20)  # Adjust position and size as needed

    def update(self, damage):
        # Update the HP bar based on damage taken
        self.current_hp = max(0, self.current_hp - damage)

    def draw(self, screen):
        # Draw the HP bar on the screen
        pygame.draw.rect(screen, self.bar_color, self.bar_rect)
        fill_width = (self.current_hp / self.max_hp) * self.bar_rect.width
        fill_rect = pygame.Rect(self.bar_rect.left, self.bar_rect.top, fill_width, self.bar_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)  # Green fill for HP

class EnemyType(Enum):
    NORMAL = 1
    FAST = 2
    STRONG = 3
    # Add more enemy types as needed


# animation work in progess

# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, images, position, frame_duration):
#         super().__init__()
#         self.images = images
#         self.image = self.images[0]
#         self.rect = self.image.get_rect()
#         self.rect.center = position
#         self.frame_duration = frame_duration
#         self.current_frame = 0
#         self.frame_timer = 0
    
#     def update(self, dt):
#         self.frame_timer += dt
#         if self.frame_timer >= self.frame_duration:
#             self.frame_timer = 0
#             self.current_frame = (self.current_frame + 1) % len(self.images)
#             self.image = self.images[self.current_frame]
