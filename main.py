import pygame
import random
import math


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


WIDTH = 800
HEIGHT = 600


# Define Node class
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None


# Define RRT class
class RRT:
    def __init__(self, start, goal, obstacles):
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.nodes = [start]
        self.step_size = 20

    def find_path(self):
        for i in range(10000):
            rand_node = Node(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            nearest_node = self.nodes[0]
            for node in self.nodes:
                if math.sqrt((rand_node.x - node.x) ** 2 + (rand_node.y - node.y) ** 2) < math.sqrt(
                        (rand_node.x - nearest_node.x) ** 2 + (rand_node.y - nearest_node.y) ** 2):
                    nearest_node = node
            new_node = Node(nearest_node.x + self.step_size * (rand_node.x - nearest_node.x) / math.sqrt(
                (rand_node.x - nearest_node.x) ** 2 + (rand_node.y - nearest_node.y) ** 2),
                            nearest_node.y + self.step_size * (rand_node.y - nearest_node.y) / math.sqrt(
                                (rand_node.x - nearest_node.x) ** 2 + (rand_node.y - nearest_node.y) ** 2))
            if self.check_collision(nearest_node, new_node):
                new_node.parent = nearest_node
                self.nodes.append(new_node)
                print(f"Random node position: ({rand_node.x}, {rand_node.y})")
                print(f"Nearest node position: ({nearest_node.x}, {nearest_node.y})")
                print(f"New node position: ({new_node.x}, {new_node.y})")

            if math.sqrt((new_node.x - self.goal.x) ** 2 + (new_node.y - self.goal.y) ** 2) < self.step_size:
                final_node = Node(self.goal.x, self.goal.y)
                final_node.parent = new_node
                self.nodes.append(final_node)
                path = [final_node]
                while path[-1].parent is not None:
                    path.append(path[-1].parent)
                return [(node.x, node.y) for node in path[::-1]]
        return None

    def check_collision(self, node1, node2):
        for obstacle in self.obstacles:
            if obstacle.collidepoint(node1.x, node1.y) or obstacle.collidepoint(node2.x, node2.y):
                return False
        return True

    def draw(self, screen):
        for node in self.nodes:
            pygame.draw.circle(screen, YELLOW, (node.x, node.y), 3)
            if node.parent is not None:
                pygame.draw.line(screen, WHITE, (node.x, node.y), (node.parent.x, node.parent.y), 2)
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, BLUE, obstacle)
        pygame.draw.circle(screen, RED, (self.start.x, self.start.y), 10)
        pygame.draw.circle(screen, GREEN, (self.goal.x, self.goal.y), 10)


# Define function to create obstacles
def create_obstacles():
    obstacles = []
    drawing = False
    start_pos = None
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not drawing:
                    start_pos = pos
                    drawing = True
                else:
                    x, y = min(start_pos[0], pos[0]), min(start_pos[1], pos[1])
                    w, h = abs(start_pos[0] - pos[0]), abs(start_pos[1] - pos[1])
                    obstacles.append(pygame.Rect(x, y, w, h))
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    for obstacle in obstacles:
                        pygame.draw.rect(screen, BLUE, obstacle)
                    # Draw new rectangle
                    pos = pygame.mouse.get_pos()
                    x, y = min(start_pos[0], pos[0]), min(start_pos[1], pos[1])
                    w, h = abs(start_pos[0] - pos[0]), abs(start_pos[1] - pos[1])
                    pygame.draw.rect(screen, BLUE, (x, y, w, h))
        pygame.display.update()
    return obstacles


# Define function to get the start and end points from user
def get_start_end_points():
    screen.fill(BLACK)
    start = None
    end = None
    selecting_start = True
    selecting_end = False
    while selecting_start or selecting_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if selecting_start:
                    start = Node(*pos)
                    pygame.draw.circle(screen, RED, pos, 10)
                    pygame.display.update()
                    selecting_start = False
                    selecting_end = True
                elif selecting_end:
                    end = Node(*pos)
                    pygame.draw.circle(screen, GREEN, pos, 10)
                    selecting_end = False

        pygame.display.update()
    return start, end


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rapidly-exploring Random Tree")

clock = pygame.time.Clock()

start, goal = get_start_end_points()
obstacles = create_obstacles()
rrt = RRT(start, goal, obstacles)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                screen.fill(BLACK)

                path = rrt.find_path()

                rrt.draw(screen)

                if path is not None:
                    pygame.draw.aalines(screen, BLUE, False, path, 3)

                pygame.display.update()

pygame.quit()
