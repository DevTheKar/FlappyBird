import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 500, 800
GRAVITY = 0.25
BIRD_WIDTH, BIRD_HEIGHT = 50, 50
PIPE_WIDTH = 70
PIPE_VELOCITY = 5
GAP = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Set up display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_img.fill(BLUE)
pipe_img = pygame.Surface((PIPE_WIDTH, HEIGHT))
pipe_img.fill(BLACK)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def jump(self):
        self.velocity = -7

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        win.blit(bird_img, (self.x, self.y))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)

    def move(self):
        self.x -= PIPE_VELOCITY

    def draw(self):
        pygame.draw.rect(win, BLACK, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(win, BLACK, (self.x, self.height + GAP, PIPE_WIDTH, HEIGHT - self.height - GAP))


# class Base:
#     VEL = 5
#     WIDTH = base_img.get_width()
#     IMG = base_img
    
#     def __init__(self, y):
#         self.y = y
#         self.x1 = 0
#         self.x2 = self.WIDTH
        
#     def move(self):
        
#         self.x1 -= self.VEL
#         self.x2 -= self.VEL
#         if self.x1 + self.WIDTH < 0:
#             self.x1 = self.x2 + self.WIDTH
            
#         if self.x2 + self.WIDTH < 0:
#             self.x2 = self.x1 + self.WIDTH
            
#     def draw(self, win):
#         win.blit(self.IMG, (self.x1, self.y))
#         win.blit(self.IMG, (self.x2, self.y))
        
def load_genome(file_path):
    # Load the saved best genome from the file
    with open(file_path, 'rb') as f:
        genome = pickle.load(f)
    return genome

def game_with_neat():
    # Initialize pygame and set up the window
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    # Load NEAT genome
    best_genome_path = 'best.pickle'
    loaded_genome = load_genome(best_genome_path)

    # Create neural network from the loaded genome
    net = neat.nn.FeedForwardNetwork.create(loaded_genome, loaded_genome.config)

    # Initialize bird and pipes
    bird = Bird(50, HEIGHT // 2)
    pipes = [Pipe(WIDTH)]

    clock = pygame.time.Clock()
    score = 0
    running = True

    while running:
        clock.tick(60)
        win.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()

        if pipes[-1].x < WIDTH - 250:
            pipes.append(Pipe(WIDTH))

        for pipe in pipes:
            pipe.move()
            if pipe.x < -PIPE_WIDTH:
                pipes.remove(pipe)
                score += 1
            if pipe.x < bird.x + BIRD_WIDTH < pipe.x + PIPE_WIDTH:
                if not (pipe.height < bird.y < pipe.height + GAP):
                    running = False

            pipe.draw()

        # Use the neural network to make decisions for the bird
        inputs = (bird.y, abs(bird.y - pipes[0].height), abs(bird.y - pipes[0].height - GAP))
        output = net.activate(inputs)

        if output[0] > 0.5:  # Tweak this threshold based on your network's behavior
            bird.jump()

        bird.draw()
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_with_neat()
        
# def blitRotateCenter(surf, image, topleft, angle):
    
#     rotated_image = pygame.transform.rotate(image, angle)
#     new_rect = rotated_image.get_rect(center = image.get_rect(topLeft = topleft).center)
    
#     surf.blit(rotated_image, new_rect.topleft)
    
# def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
        
#         if gen == 0:
#         gen = 1
#     win.blit(bg_img, (0,0))

#     for pipe in pipes:
#         pipe.draw(win)

#     base.draw(win)
#     for bird in birds:
#         # draw lines from bird to pipe
#         if DRAW_LINES:
#             try:
#                 pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
#                 pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
#             except:
#                 pass
#         # draw bird
#         bird.draw(win)

#     # score
#     score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
#     win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

#     # generations
#     score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
#     win.blit(score_label, (10, 10))

#     # alive
#     score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
#     win.blit(score_label, (10, 50))

#     pygame.display.update()
    
# def run(config_file):
    