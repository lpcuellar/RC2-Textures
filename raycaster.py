import pygame

from math import cos, sin, pi

##  declaración de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG = (96, 96, 96)

textures = {
    '1' : pygame.image.load('./textures/stone_iron_wall.png'),
    '2' : pygame.image.load('./textures/stone_torch.png'),
    '3' : pygame.image.load('./textures/iron_x.png'),
    '4' : pygame.image.load('./textures/iron_wall.png'),
}

class RayCaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.block_size = 50
        self.wall_height = 50

        self.step_size = 5

        self.player = {
            'x': 75,
            'y': 175, 
            'angle': 0,
            'fov': 60,
        }

    def loadMap(self, filename):
        with open(filename) as mapFile:
            for line in mapFile.readlines():
                self.map.append(list(line))

    def drawRect(self, x, y, tex):
        tex = pygame.transform.scale(tex, (self.block_size, self.block_size))
        rect = tex.get_rect()
        rect = rect.move((x, y))
        self.screen.blit(tex, rect)

    def drawPlayerIcon(self, color):
        rect = (int(self.player['x'] - 2), int(self.player['y'] - 2), 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0

        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                hit_x = x - i * self.block_size
                hit_y = y - j * self.block_size

                if 1 < hit_x < self.block_size - 1:
                    max_hit = hit_x
                else:
                    max_hit = hit_y
                
                tx = max_hit / self.block_size

                return dist, self.map[j][i], tx
            
            self.screen.set_at((x, y), WHITE)
            dist += 2

    def render(self):
        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        for x in range(0, half_width, self.block_size):
            for y in range(0, self.height, self.block_size):
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if self.map[j][i] != ' ':
                    self.drawRect(x, y, textures[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        for i in range(half_width):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / half_width
            dist, wallType, tx = self.castRay(angle)

            x = half_width + i

            h = self.height / (dist * cos((angle - self.player['angle']) * pi / 180)) * self.wall_height

            start = int(half_height - h / 2)
            finish = int(half_height + h / 2)

            img = textures[wallType]
            tx = int(tx * img.get_width())

            for y in range(start, finish):
                ty = (y - start) / (finish - start)
                ty = int(ty * img.get_height())
                tex_color = img.get_at((tx, ty))
                self.screen.set_at((x, y), tex_color)

        for i in range(self.height):
            self.screen.set_at((half_width, i), BLACK)
            self.screen.set_at((half_width + 1, i), BLACK)
            self.screen.set_at((half_width - 1, i), BLACK)
            


pygame.init()
screen = pygame.display.set_mode((1600, 800), pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color('white'))
    
    return fps


ray = RayCaster(screen)
ray.loadMap('map.txt')

isRunning = True

while isRunning:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False
        
        new_x = ray.player['x']
        new_y = ray.player['y']

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            
            elif ev.key == pygame.K_w:
                new_x += cos(ray.player['angle'] * pi / 180) * ray.step_size
                new_y += sin(ray.player['angle'] * pi / 180) * ray.step_size
            
            elif ev.key == pygame.K_s:
                new_x -= cos(ray.player['angle'] * pi / 180) * ray.step_size
                new_y -= sin(ray.player['angle'] * pi / 180) * ray.step_size
           
            elif ev.key == pygame.K_a:
                new_x -= cos((ray.player['angle'] + 90) * pi / 180) * ray.step_size
                new_y -= sin((ray.player['angle'] + 90) * pi / 180) * ray.step_size
            
            elif ev.key == pygame.K_d:
                new_x += cos((ray.player['angle'] + 90) * pi / 180) * ray.step_size
                new_y += sin((ray.player['angle'] + 90) * pi / 180) * ray.step_size
            
            elif ev.key == pygame.K_q:
                ray.player['angle'] -= 5
            
            elif ev.key == pygame.K_e:
                ray.player['angle'] += 5

            i = int(new_x / ray.block_size)
            j = int(new_y / ray.block_size)

            if ray.map[j][i] == ' ':
                ray.player['x'] = new_x
                ray.player['y'] = new_y

    screen.fill(pygame.Color('gray'))
    screen.fill(pygame.Color('gray'), (int(ray.width / 2), 0, int(ray.width / 2), int(ray.height / 2)))
    screen.fill(pygame.Color('dimgray'), (int(ray.width / 2), int(ray.height / 2), int(ray.width / 2), int(ray.height / 2)))

    ray.render()

    screen.fill(pygame.Color('black'), ( 0, 0, 30, 30))
    screen.blit(updateFPS(), (0, 0))
    clock.tick(30)

    pygame.display.flip()

pygame.quit() 