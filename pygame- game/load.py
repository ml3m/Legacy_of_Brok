import pygame

ASSETS_PATH = "Legacy_of_Brok/pygame- game/assets/"

background_image = pygame.image.load(ASSETS_PATH + "background1.jpg")

enemy_image1 = pygame.image.load(ASSETS_PATH + "enemy.png")
enemy_image2 = pygame.image.load(ASSETS_PATH + "enemy2.png")
magma_enemy = pygame.image.load(ASSETS_PATH + "enemy3.gif")
enemy_image4 = pygame.image.load(ASSETS_PATH + "enemy4.png")
enemy_image5 = pygame.image.load(ASSETS_PATH + "enemy5.png")
misterious_enemy = pygame.image.load(ASSETS_PATH + "misterious_enemy.gif")

# Scale the images
player_image = pygame.image.load(ASSETS_PATH + "character.png")
player_image = pygame.transform.scale(player_image, (90, 110))

reset_image = pygame.image.load(ASSETS_PATH + "reset.png")
reset_image = pygame.transform.scale(reset_image, (300, 100))

gun_image = pygame.image.load(ASSETS_PATH + "gun.png")
gun_image = pygame.transform.scale(gun_image, (120, 120))

gun_image_rev = pygame.image.load(ASSETS_PATH + "gun-rev.png")
gun_image_rev = pygame.transform.scale(gun_image_rev, (120, 120))

projectile_image = pygame.image.load(ASSETS_PATH + "bullet.png")
projectile_image = pygame.transform.scale(projectile_image, (20, 20))

drop_image = pygame.image.load(ASSETS_PATH + "drop.png")
drop_image = pygame.transform.scale(drop_image, (40, 40))

shot_effect = pygame.image.load(ASSETS_PATH + "shot_effect.png")
shot_effect = pygame.transform.scale(shot_effect, (50, 100))

magma_projectile_img = pygame.image.load(ASSETS_PATH + "magma_projectile.png")
magma_projectile_img = pygame.transform.scale(magma_projectile_img, (28, 28))

magma_ball = pygame.image.load(ASSETS_PATH + "magma_ball.png")
magma_ball = pygame.transform.scale(magma_ball, (25, 29))

enemy_images = [
    pygame.transform.scale(enemy_image1, (100, 100)),
    pygame.transform.scale(enemy_image2, (100, 100)),
    pygame.transform.scale(magma_enemy, (100, 100)),
    pygame.transform.scale(enemy_image4, (85, 100)),
    pygame.transform.scale(enemy_image5, (100, 100)),
]
