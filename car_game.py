import pygame
from pygame.locals import *
import random
import clock

pygame.init()

width = 700
height = 780
screen_size = (width, height)


font = pygame.font.Font('freesansbold.ttf', 28)
score = 0
speed = 4
paused = False
screen = pygame.display.set_mode(screen_size)
background = pygame.image.load('./Images/background.jpg')
background = pygame.transform.scale(background, (width, height))

background_y = 0
background_speed = 1.5


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        image_scale = 150 / self.image.get_rect().width
        new_width = self.image.get_rect().width * image_scale
        new_height = self.image.get_rect().height * image_scale
        self.image = pygame.transform.scale(
            self.image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('./Images/racer 2.png')
        super().__init__(image, x, y)


playerGroup = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

player = PlayerVehicle(240, 550)
playerGroup.add(player)

vehicle_images = []
img_file = ['enemy.png']
for img in img_file:
    image = pygame.image.load('Images/'+img)
    vehicle_images.append(image)

crash = pygame.image.load('./Images/crash.png')
crash = pygame.transform.scale(crash, (100, 100))
crash_rect = crash.get_rect()

clock = pygame.time.Clock()
fps = 240

running = True
gameover = False

while running:
    clock.tick(fps)

    screen.fill((0, 0, 0))
    background_y += background_speed
    if background_y > height:
        background_y = 0

    # Draw background
    screen.blit(background, (0, background_y - height))
    screen.blit(background, (0, background_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and player.rect.x < 400:
                player.rect.x += 240

            if event.key == pygame.K_LEFT and player.rect.x > 240:
                player.rect.x -= 240

            if event.key == pygame.K_UP and player.rect.y > 40:
                player.rect.y -= 60

            if event.key == pygame.K_DOWN and player.rect.y < 760:
                player.rect.y += 60

            # if event.key == pygame.K_SPACE:
            #     # Toggle pause state
            #     paused = not paused

            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True

                    if event.key == pygame.K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [
                            player.rect.left, (player.rect.center[1]+vehicle.rect.center[1])//2]

                    elif event.key == pygame.K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [
                            player.rect.right, (player.rect.center[1]+vehicle.rect.center[1])//2]

    playerGroup.update(screen)
    # if not paused:
    playerGroup.draw(screen)
    if len(vehicle_group) < 1:

        add_vehicle = True
        if add_vehicle:
            lane = random.choice([240, 480])
            img = random.choice(vehicle_images)
            vehicle = Vehicle(img, lane, 20)
            vehicle_group.add(vehicle)

    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= 780:
            vehicle.kill()
            score = score + 1

            if score > 5 and score % 5 == 0:
                speed += 0.5

    vehicle_group.draw(screen)
    vehicle_group.update(screen)
    score_rendered = font.render(
        "Score : " + str(score), True, (0, 0, 0))
    screen.blit(score_rendered, (10, 10))

    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        paused = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    if gameover:
        screen.blit(crash, crash_rect)
        crash_rendered = font.render(
            "Game Over: Press Y to Continue, N to exit", True, (255, 0, 0))
        screen.blit(crash_rendered, (50, 100))

    pygame.display.update()

    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                gameover = False

            if event.type == KEYDOWN:
                if event.key == pygame.K_y:
                    gameover = False
                    speed = 4
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [240, 550]

                elif event.key == pygame.K_n:
                    # exit the loops
                    gameover = False
                    running = False

pygame.quit()
