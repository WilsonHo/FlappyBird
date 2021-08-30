import sys
import random
import pygame


def draw_floor(floor, floor_x_pos):
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    print random_pipe_pos
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 650))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 650:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False

    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        return False

    return True


def rotate_bird(b):
    new_bird = pygame.transform.rotozoom(b, -bird_movement * 4, 1)
    return new_bird

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score

    return high_score

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render('Score: {}'.format(str(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('High Score: {}'.format(str(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 500))
        screen.blit(high_score_surface, high_score_rect)

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

screen = pygame.display.set_mode((432, 768))
gravity = 0.25
bird_movement = 0
game_active = True
pipe_height = [350, 400, 450, 500, 550]
clock = pygame.time.Clock()
bg = pygame.image.load('../resources/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load('../resources/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

bird_down = pygame.transform.scale2x(pygame.image.load('../resources/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('../resources/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('../resources/yellowbird-upflap.png').convert_alpha())
birds = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = birds[bird_index]
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200 )

bird_rect = bird.get_rect(center=(100, 384))

pipe_surface = pygame.image.load('../resources/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)
pipes = []

game_font = pygame.font.Font('../resources/04B_19.TTF', 40)
score = 0
high_score = 0

def bird_animation():
    new_bird = birds[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


game_over_surface = pygame.transform.scale2x(pygame.image.load('../resources/message.png').convert_alpha())
game_over_surface_rect = game_over_surface.get_rect(center=(216, 384))

flap_sound = pygame.mixer.Sound('../resources/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('../resources/sfx_hit.wav')
score_sound = pygame.mixer.Sound('../resources/sfx_point.wav')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipes = []
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipes.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipes)
        pipes = move_pipe(pipes)
        draw_pipe(pipes)
        score += 0.01
        score_display('main game')
    else:
        screen.blit(game_over_surface, game_over_surface_rect)
        high_score = update_high_score(score, high_score)
        score_display('game over')

    floor_x_pos -= 1
    draw_floor(floor, floor_x_pos)

    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(1200)
