
# Check random paths forever and draw the shortest one found

import pygame, random
WIDTH, HEIGHT = 1400, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traveling Salesman")

class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

def generate_point():
  x = random.randrange(point_radius, WIDTH - point_radius)
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
  return calculate_distance()

def draw_points():
  for point in points:
    pygame.draw.circle(screen, (255, 255, 255), (point.x, point.y), point_radius)
    pygame.draw.circle(screen, (0, 0, 0), (point.x, point.y), point_radius - 3)

def draw_orderd_path():
  for i in range(total_points - 1):
    point_one = (points[i].x, points[i].y)
    point_two = (points[i + 1].x, points[i + 1].y)
    pygame.draw.line(screen, (255, 255, 255), point_one, point_two, 1)

def draw_record_path():
  for i in range(total_points - 1):
    point_one = (record_point_set[i].x, record_point_set[i].y)
    point_two = (record_point_set[i + 1].x, record_point_set[i + 1].y)
    pygame.draw.line(screen, (255, 100, 50), point_one, point_two, 10)

def calculate_distance():
  total = 0
  for i in range(total_points - 1):
    difference_one = points[i].x - points[i + 1].x
    difference_two = points[i].y - points[i + 1].y
    distance = (difference_one ** 2 + difference_two ** 2) ** 0.5
    total += distance;
  return total

points, point_radius, total_points = [], 10, 6
record_distance = generate_points()
record_point_set = points.copy()

while True:
  screen.fill((0, 0, 0))
  draw_record_path()
  draw_orderd_path()
  draw_points()
  pygame.display.update()

  for event in pygame.event.get():
    if event.type == pygame.QUIT: quit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      record_distance = generate_points()

  # Switch two random points to randomize order
  a = random.randrange(0, total_points)
  b = random.randrange(0, total_points)
  points[a], points[b] = points[b], points[a]
  
  new_distance = calculate_distance()
  if new_distance < record_distance:
    record_distance = new_distance
    record_point_set = points.copy()
    print(record_distance)
