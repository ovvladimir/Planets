import math
import os
import random
import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.image.blit(background, self.rect)
        # self.image.fill((0, 0, 0))
        self.stars_list = []
        for _ in range(150):
            self.stars_list.append(pygame.draw.circle(
                self.image, (128, 128, 0),
                (random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)),
                random.randint(1, 2)))


class Sun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = sun_image
        self.index = 0
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def update(self):
        self.index += 0.1
        self.image = self.images[int(self.index % self.range)]


class Planets(pygame.sprite.Sprite):
    def __init__(self, image, position, angle, speed):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.x, self.y = position
        self.speed = speed
        self.image = pygame.transform.rotate(image, 180)
        self.orig_image = self.image
        self.rect = self.image.get_rect()

    def update(self):
        self.angle += 365 / self.speed
        self.angle %= 360
        x = SCREEN_WIDTH // 2 + self.x * math.cos(math.radians(self.angle))
        y = SCREEN_HEIGHT // 2 - self.y * math.sin(math.radians(self.angle))
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=(x, y))


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
path = os.path.dirname(os.path.abspath(__file__))
background = pygame.image.load(os.path.join(path, 'images', 'bg.png'))
SCREEN_WIDTH = background.get_width()
SCREEN_HEIGHT = background.get_height()
pygame.display.set_caption('Solar System')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
FPS = 120
clock = pygame.time.Clock()

all_sprite = pygame.sprite.Group()
bg = Background()
all_sprite.add(bg)

planets_image = []
planets_path = os.path.join(path, 'images', 'planets')
for file_name in os.listdir(planets_path):
    im = pygame.image.load(os.path.join(planets_path, file_name))
    planets_image.append(im)
days_list = [88., -225., 365., 687., 4333., 10760., -30799., 60192.]
angle_list = [0, 32, 76, 102, 47, 180, 220, 330]
pos_list = [
    (120, 80), (150, 100), (190, 130), (240, 160),
    (290, 200), (400, 265), (480, 320), (565, 375)]
for i, img in enumerate(planets_image):
    planet = Planets(img, pos_list[i], angle_list[i], days_list[i])
    all_sprite.add(planet)

sun_image = []
sun_path = os.path.join(path, 'images', 'sun')
for file_name in os.listdir(sun_path):
    im = pygame.image.load(os.path.join(sun_path, file_name))
    sun_image.append(im)
sun = Sun()
all_sprite.add(sun)

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT or \
            e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
        break

    all_sprite.update()
    all_sprite.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
    # pygame.display.set_caption(f'Solar System      FPS: {int(clock.get_fps())}')
