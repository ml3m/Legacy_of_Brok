import pygame

background_image = pygame.image.load("assets/background1.jpg" )

enemy_image1 = pygame.image.load("assets/enemy.png")
enemy_image2 = pygame.image.load("assets/enemy2.png")
magma_enemy = pygame.image.load("assets/enemy3.gif")
enemy_image4 = pygame.image.load("assets/enemy4.png")
enemy_image5 = pygame.image.load("assets/enemy5.png")
misterious_enemy = pygame.image.load("assets/misterious_enemy.gif")

# Scale the images
player_image = pygame.image.load("assets/character.png")
player_image = pygame.transform.scale(player_image, (90, 110))

reset_image = pygame.image.load("assets/reset.png")
reset_image = pygame.transform.scale(reset_image, (300, 100))

gun_image = pygame.image.load("assets/gun.png")
gun_image = pygame.transform.scale(gun_image, (120, 120))

gun_image_rev = pygame.image.load("assets/gun-rev.png")
gun_image_rev = pygame.transform.scale(gun_image_rev, (120, 120))

projectile_image = pygame.image.load("assets/bullet.png")
projectile_image = pygame.transform.scale(projectile_image, (20, 20))

drop_image = pygame.image.load("assets/drop.png")
drop_image = pygame.transform.scale(drop_image, (40, 40))

shot_effect = pygame.image.load("assets/shot_effect.png")
shot_effect = pygame.transform.scale(shot_effect, (50, 100))

magma_projectile_img = pygame.image.load("assets/magma_projectile.png")
magma_projectile_img = pygame.transform.scale(magma_projectile_img, (28, 28))

magma_ball = pygame.image.load("assets/magma_ball.png")
magma_ball = pygame.transform.scale(magma_ball, (25, 29))

enemy_images = [
    pygame.transform.scale(enemy_image1, (100, 100)),
    pygame.transform.scale(enemy_image2, (100, 100)),
    pygame.transform.scale(magma_enemy, (100, 100)),
    pygame.transform.scale(enemy_image4, (85, 100)),
    pygame.transform.scale(enemy_image5, (100, 100)),
]
