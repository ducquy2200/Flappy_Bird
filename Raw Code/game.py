import pygame
import sys
import os
import random


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

#------------------------------------------------------------------------------------------------------------------
running_game = False
stop_program = False
welcome_screen = True
clock = pygame.time.Clock()

#------------------------------------------------------------------------------------------------------------------
hscore = 0
score = 0
score_sub = 0
score_reset = True
letter_style = pygame.font.Font("Flappy_Font.ttf", 35)

#------------------------------------------------------------------------------------------------------------------
width = 576
height = 1024
dimension = (width, height)
window = pygame.display.set_mode(dimension)
pygame.display.set_caption("Flappy Bird")

#------------------------------------------------------------------------------------------------------------------
get_ready = pygame.image.load(os.path.join("Game Images", "start-game.png")).convert_alpha()
get_ready = pygame.transform.scale2x(get_ready)

#------------------------------------------------------------------------------------------------------------------
game_over = pygame.image.load(os.path.join("Game Images", "game-over.png")).convert_alpha()
game_over = pygame.transform.scale2x(game_over)

#------------------------------------------------------------------------------------------------------------------
bg = random.randint(0, 1)
bg_day = pygame.image.load(os.path.join("Game Images", "bg-day.png")).convert()
bg_day = pygame.transform.scale2x(bg_day)
bg_night = pygame.image.load(os.path.join("Game Images", "bg-night.png")).convert()
bg_night = pygame.transform.scale2x(bg_night)

#------------------------------------------------------------------------------------------------------------------
ground = pygame.image.load(os.path.join("Game Images", "ground.png")).convert()
ground = pygame.transform.scale2x(ground)
ground_position = 0

#------------------------------------------------------------------------------------------------------------------
game_gravity = 0.2
bird_y_movement = 0
bird_color = ["red", "yellow", "blue"]
bird_color_choice = bird_color[random.randint(0, 2)]
bird_flap_mid = pygame.image.load(os.path.join("Game Images", bird_color_choice+"-bird-mid-flap.png")).convert_alpha()
bird_flap_mid = pygame.transform.scale2x(bird_flap_mid)
bird_flap_up = pygame.image.load(os.path.join("Game Images", bird_color_choice+"-bird-up-flap.png")).convert_alpha()
bird_flap_up = pygame.transform.scale2x(bird_flap_up)
bird_flap_down = pygame.image.load(os.path.join("Game Images", bird_color_choice+"-bird-down-flap.png")).convert_alpha()
bird_flap_down = pygame.transform.scale2x(bird_flap_down)
bird_list = [bird_flap_up, bird_flap_mid, bird_flap_down]
bird_choice = 1
bird = bird_list[bird_choice]
bird_rect = bird.get_rect(center=(100, height/2))
bird_cycle = pygame.USEREVENT + 1
pygame.time.set_timer(bird_cycle, 200)

#------------------------------------------------------------------------------------------------------------------
pillar_color = ["green", "red"]
pillar_color_choice = pillar_color[random.randint(0, 1)]
pillar = pygame.image.load(os.path.join("Game Images", "pillar-"+pillar_color_choice+".png")).convert()
pillar = pygame.transform.scale2x(pillar)
pillar_list = []
pillar_spawn = pygame.USEREVENT
pygame.time.set_timer(pillar_spawn, 3000)
pillar_height = [350, 400, 450, 500, 550, 600, 650, 700, 750, 800]

#------------------------------------------------------------------------------------------------------------------
sound_die = pygame.mixer.Sound(os.path.join("Game Audios", "die.wav"))
sound_hit = pygame.mixer.Sound(os.path.join("Game Audios", "hit.wav"))
sound_point = pygame.mixer.Sound(os.path.join("Game Audios", "point.wav"))
sound_swooshing = pygame.mixer.Sound(os.path.join("Game Audios", "swooshing.wav"))
sound_wing = pygame.mixer.Sound(os.path.join("Game Audios", "wing.wav"))

#------------------------------------------------------------------------------------------------------------------
def start_screen(x, y):
    window.blit(get_ready, (x, y))
    start_instruction = letter_style.render("Press Enter to start!", True, (255, 255, 255))
    start_instruction_rect = start_instruction.get_rect(center=(width/2, 900))
    window.blit(start_instruction, start_instruction_rect)

#------------------------------------------------------------------------------------------------------------------
def over_screen(x, y):
    window.blit(game_over, (x, y))
    reset_instruction = letter_style.render("Press Enter to try again!", True, (255, 255, 255))
    reset_instruction_rect = reset_instruction.get_rect(center=(width/2, 850))
    window.blit(reset_instruction, reset_instruction_rect)

#------------------------------------------------------------------------------------------------------------------
def background(x, y):
    if (bg == 0):
        window.blit(bg_day, (x, y))
    else:
        window.blit(bg_night, (x, y))

#------------------------------------------------------------------------------------------------------------------
def ground_base(x, y):
    window.blit(ground, (x, y))
    window.blit(ground, (x+width, y))

#------------------------------------------------------------------------------------------------------------------
def pillar_creation():
    pillar_level = random.randint(0, 9)
    bottom_pillar_rect = pillar.get_rect(midtop=(1050, pillar_height[pillar_level]))
    top_pillar_rect = pillar.get_rect(midbottom=(1050, pillar_height[pillar_level]-250))
    return bottom_pillar_rect, top_pillar_rect

#------------------------------------------------------------------------------------------------------------------
def pillar_movement(pillar_set):
    for p in pillar_set:
        p.centerx -= 2
    return pillar_set

#------------------------------------------------------------------------------------------------------------------
def pillar_display(pillar_set):
    for p in pillar_set:
        if p.top <= 0:
            pillar_flip = pygame.transform.flip(pillar, False, True)
            window.blit(pillar_flip, p)
        else:
            window.blit(pillar, p)

#------------------------------------------------------------------------------------------------------------------
def collision(pillar_set):
    for p in pillar_set:
        if (bird_rect.colliderect(p) == True):
            sound_hit.play(0)
            sound_die.play(0)
            return False

    if (bird_rect.bottom >= 900) or (bird_rect.top <= -200):
        sound_hit.play(0)
        sound_die.play(0)
        return False

    return True

#------------------------------------------------------------------------------------------------------------------
def bird_rotation(bird_image):
    rotated_bird = pygame.transform.rotozoom(bird_image, -(bird_y_movement*5), 1)
    return rotated_bird

#------------------------------------------------------------------------------------------------------------------
def bird_action(bird_image_rect, bird_image_list):
    bird_selected = bird_image_list[bird_choice]
    bird_selected_rect = bird_selected.get_rect(center=(bird_image_rect.center))
    return bird_selected, bird_selected_rect

#------------------------------------------------------------------------------------------------------------------
def score_counter(pillar_set, counter):
    for p in pillar_set:
        if p.centerx == bird_rect.centerx:
            sound_point.play(0)
            sound_swooshing.play(0)
            counter += 1
    return counter

#------------------------------------------------------------------------------------------------------------------
def all_score_text_display(x, score_y, hscore_y):
    score_text = letter_style.render("Score", True, (255, 255, 255))
    score_text_rect = score_text.get_rect(center=(x, score_y))
    window.blit(score_text, score_text_rect)
    hscore_text = letter_style.render("High Score", True, (255, 255, 255))
    hscore_text_rect = hscore_text.get_rect(center=(x, hscore_y))
    window.blit(hscore_text, hscore_text_rect)

#------------------------------------------------------------------------------------------------------------------
def score_num_display(x, score_y):
    score_num = letter_style.render(str(score), True, (255, 255, 255))
    score_num_rect = score_num.get_rect(center=(x, score_y))
    window.blit(score_num, score_num_rect)

#------------------------------------------------------------------------------------------------------------------
def hscore_num_display(x, hscore_y):
    hscore_num = letter_style.render(str(hscore), True, (255, 255, 255))
    hscore_num_rect = hscore_num.get_rect(center=(x, hscore_y))
    window.blit(hscore_num, hscore_num_rect)

#------------------------------------------------------------------------------------------------------------------
while (stop_program != True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_program = True
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE) and (running_game == True):
                sound_wing.play(0)
                bird_y_movement = 0
                bird_y_movement -= 8
            if (event.key == pygame.K_RETURN) and (running_game == False):
                welcome_screen = False
                pillar_list.clear()
                bird_rect.center = (100, height/2)
                bird_y_movement = 0
                running_game = True
            if (event.key == pygame.K_ESCAPE):
                pyagme.quit()

        if event.type == pillar_spawn:
            pillar_list.extend(pillar_creation())
        if event.type == bird_cycle:
            bird, bird_rect = bird_action(bird_rect, bird_list)
            bird_choice += 1
            if bird_choice == 2:
                bird_choice = 0
                bird_list = list(reversed(bird_list))

    background(0, 0)

    if (welcome_screen == True):
        start_screen(104, 245)

    if (running_game == True):

        if (score_reset == True):
            score = 0
            score_sub = 0

        pillar_list = pillar_movement(pillar_list)
        pillar_display(pillar_list)

        ground_base(ground_position, 900)
        ground_position -= 2
        if ground_position <= (-width+3):
            ground_position = 0

        bird_flying_direction = bird_rotation(bird)
        window.blit(bird_flying_direction, bird_rect)
        bird_y_movement += game_gravity
        bird_rect.centery += bird_y_movement
        running_game = collision(pillar_list)

        score_sub = score_counter(pillar_list, score_sub)
        score = int(score_sub/2)

        score_num_display(width/2, 200)

        if (score >= hscore):
            hscore = score

        score_reset = False

    elif (welcome_screen == False) and (running_game == False):

        over_screen(96, 200)
        all_score_text_display(width/2, 375, 525)
        score_num_display(width/2, 450)
        hscore_num_display(width/2, 600)
        score_reset = True

    pygame.display.update()
    clock.tick(150)

#------------------------------------------------------------------------------------------------------------------
pygame.quit()
sys.exit()
