import pygame
import random
from pygame.locals import *
import math
import neat
import os
import pickle

pygame.init()
clock = pygame.time.Clock()
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (31, 84, 32)
yellow1 = (255, 255, 102)
car_width = 40
car_height = 40
# drawing screen and making the game
screen = pygame.display.set_mode((750, 400))
steering = 3
cars = []


class Car:
    def __init__(self, x, y, n, nets, ge):
        self.image = pygame.image.load('assets/red-car.png')
        self.image = pygame.transform.scale(self.image, (car_width, car_height))
        self.ang = 0
        self.image = pygame.transform.rotate(self.image, self.ang)
        self.x = x
        self.y = y
        self.vel = 5
        self.steer1 = 10
        self.move(n, nets, ge)

    def move(self, n, nets, ge):
        #self.steer()
        #calculating location based on speed and angle
        self.x += math.cos(math.radians(360 - self.ang)) * self.vel
        self.y += math.sin(math.radians(360 - self.ang)) * self.vel
        #rotating the car's image
        self.image2 = pygame.transform.rotate(self.image, self.ang)
        self.rect = self.image2.get_rect(center=(self.x, self.y))
        self.check_collision(bg, n, nets, ge)

        #building the radar
        line_len = 250
        end_pos0 = [0, 15, 40, 90, 270, 320, 345]
        end_pos1 = []
        self.radar_len = ()
        #calculating radar end coordinate
        for n in end_pos0:
            for line_len1 in range(line_len):
                linex = self.x + math.cos(math.radians(360 - self.ang + n)) * line_len1
                liney = self.y + math.sin(math.radians(360 - self.ang + n)) * line_len1
                if 0 < linex < 749 and 0 < liney < 399 and bg.get_at((int(linex), int(liney))) == (255, 255, 255, 255):
                    end_pos1.append([int(linex), int(liney)])
                    self.radar_len = self.radar_len + (line_len1,)
                    break
                elif line_len1 is 249:
                    self.radar_len = self.radar_len + (line_len1,)
                    break
        #drawing the radar to screen
        for n in end_pos1:
            pygame.draw.line(screen, green, [self.x, self.y], [n[0], n[1]])

    def check_collision(self, bg, n, nets, ge):
        len = 17
        #calculating 4 points of detection
        left_front = [self.rect.center[0] + math.cos(math.radians(360 - (self.ang + 20))) * len,
                    self.rect.center[1] + math.sin(math.radians(360 - (self.ang + 20))) * len]
        left_rear = [self.rect.center[0] + math.cos(math.radians(360 - (self.ang + 160))) * len,
                    self.rect.center[1] + math.sin(math.radians(360 - (self.ang + 160))) * len]
        right_front = [self.rect.center[0] + math.cos(math.radians(360 - (self.ang + 340))) * len,
                    self.rect.center[1] + math.sin(math.radians(360 - (self.ang + 340))) * len]
        right_rear = [self.rect.center[0] + math.cos(math.radians(360 - (self.ang + 200))) * len,
                       self.rect.center[1] + math.sin(math.radians(360 - (self.ang + 200))) * len]
        coll_points = [left_front, left_rear, right_rear, right_front]
        for point in coll_points:
            #showing the points to the screen
            #pygame.draw.circle(screen, blue, [int(point[0]), int(point[1])], 5, 2)
            #checking if one of the points detect white (means the car is off the track
            if bg.get_at((int(point[0]), int(point[1]))) == (255, 255, 255, 255):
                loose(n, nets, ge)


    #calculating steering level at low and high velocities
    def steer(self):
        self.steer1 = self. vel * steering
        if self.steer1 > 9:
            self.steer1 = 9
        return self.steer1

    def acc(self):
        if self.vel < 18:
            self.vel += 1
        else:
            self.vel = 18
        return None

    def brake(self):
        if self.vel > 5:
            self.vel -= 1
        else:
            self.vel = 5
        return None

# backgroung image
bg = pygame.image.load("assets/gray good map.png")
bg = pygame.transform.scale(bg, (750, 400))


def draw_all(cars):
    #NEED FIXING!!
    if len(cars) > 0:
        for n in range(20):
            screen.blit(cars[n].image2, cars[n].rect)


def move_all(n, nets, ge):
    cars[n].move(n, nets, ge)


def loose(n, nets, ge):
    if len(cars) > 0 and len(cars) is not n:
        #print(len(cars), n)
        cars.pop(n)
        nets.pop(n)
        ge.pop(n)



def main(genomes, config):
    nets = []
    ge = []
    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(130, 340, _, nets, ge))
        ge.append(g)
    run_game = True
    while run_game and len(cars) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            cars[0].vel += 3

        screen.blit(bg, (0, 0))
        if len(cars) > 0:
            for n, car in enumerate(cars):
                fit_val = car.vel * 0.3 - 2.4
                ge[n].fitness += fit_val
                #ai choises:
                output = nets[n].activate(car.radar_len)
                if output[0] > 0.5:
                    #print("right")
                    car.ang -= car.steer1
                elif output[0] < -0.5:
                    #print("left")
                    car.ang += car.steer1
                if output[1] > 0.5:
                    car.acc()
                    #car.vel += 1
                elif output[1] < -0.5:
                    car.brake()
                move_all(n, nets, ge)
            draw_all(cars)
        pygame.display.update()
        clock.tick(30)




# *********************** NEAT    NEAT    NEAT    NEAT ********************* #

# running he NEAT func
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    #   SET A VARIABLE TO THE POPULATION
    po = neat.Population(config)

    #   GIVES STATS ABOUT THE POPULATION
    po.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    po.add_reporter(stats)

    #   HOW MANY GENERATIONS

    winner = po.run(main, 100)
    pickle.dump(winner, open("best car speed1.pickle", "wb"))

# giving NEAT access to the config file
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward2.txt')
    run(config_path)