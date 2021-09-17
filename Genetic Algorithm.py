
# Check paths that stem from better generations

import pygame, random, math
WIDTH, HEIGHT = 1400, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traveling Salesman")

population, fitness, population_size = [], [], 1000
record_distance, record_point_set = float('inf'), []
points, point_radius, total_points = [], 10, 9
column_offset, mutation_rate = 300, .1

class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

def generate_point():
  x = random.randrange(point_radius, WIDTH - point_radius - column_offset)
  y = random.randrange(point_radius, HEIGHT - point_radius)
  point, collide = Point(x, y), False
  for p in points:
    if p.x - point_radius * 2 <= point.x <= p.x + point_radius * 2:
      if p.y - point_radius * 2 <= point.y <= p.y + point_radius * 2:
        collide = True
  if collide: generate_point()
  else: points.append(point)

def generate_points():
  points.clear()
  for i in range(total_points):
    generate_point()

def draw_points():
  for point in points:
    pygame.draw.circle(screen, (255, 255, 255), (point.x, point.y), point_radius)
    pygame.draw.circle(screen, (0, 0, 0), (point.x, point.y), point_radius - 3)

def draw_record_path():
  for i in range(total_points - 1):
    point_one = (points[record_point_set[i]].x, points[record_point_set[i]].y)
    point_two = (points[record_point_set[i + 1]].x, points[record_point_set[i + 1]].y)
    pygame.draw.line(screen, (50, 100, 255), point_one, point_two, 6)

def calculate_distance(order):
  total = 0
  for i in range(total_points - 1):
    difference_one = points[order[i]].x - points[order[i + 1]].x
    difference_two = points[order[i]].y - points[order[i + 1]].y
    distance = (difference_one ** 2 + difference_two ** 2) ** 0.5
    total += distance;
  return total

def generate_population(size):
  population.clear()
  for i in range(size):
    random_arangement = [ i for i in range(total_points) ]
    random.shuffle(random_arangement)
    population.append(random_arangement)

def calculate_fitness():
  global record_distance, record_point_set
  for i in range(len(population)):
    distance = calculate_distance(population[i])
    fitness.append(1 / distance)
    if distance < record_distance:
      record_distance = distance
      record_point_set = population[i]
  total = sum(fitness)
  for i in range(len(fitness)):
    fitness[i] /= total

def next_generation():
  global population
  new_population = []
  for i in range(len(population)):
    order = mutate(select(population, fitness), mutation_rate)
    new_population.append(order)
  population = new_population
  fitness.clear()

def select(pop, fit_levels):
  index, rand_float = 0, random.random()
  while rand_float > 0:
    rand_float -= fit_levels[index]
    index += 1
  return pop[index - 1].copy()

def mutate(order, mutation_rate):
  for i in range(total_points):
    if random.random() < mutation_rate:
      a = random.randrange(0, len(order))
      b = random.randrange(0, len(order))
      order[a], order[b] = order[b], order[a]
  return order

def draw_elements():
  screen.fill((0, 0, 0))
  draw_record_path()
  draw_points()
  pygame.display.update()

def initialize():
  global record_distance
  generate_population(population_size)
  record_distance = float('inf')
  generate_points()


initialize()

while True:
  calculate_fitness()
  next_generation()
  draw_elements()
  for event in pygame.event.get():
    if event.type == pygame.QUIT: quit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      initialize()
