import pygame
import gamebox
import random


camera = gamebox.Camera(800, 600)
game_on = False
game_on2 = False
checkpoint = False
win = False

############### MAP GENERATION #################
grass = []
for i in range(6):  # Generates Grass
    patch = gamebox.from_image(400, 1200 - i * 600, 'grass.png')
    grass.append(patch)

steps = gamebox.from_image(400, 850, 'rotunda.png')

roofs = []
for i in range(8):  # Generates Lawn Houses
    x = gamebox.from_image(15, 660 - i * 280, 'longroof.png')
    y = gamebox.from_image(785, 660 - i * 280, 'longroof.png')
    roofs.append(x)
    roofs.append(y)

for roof in roofs:
    roof.scale_by(.4)
for each in grass:
    each.scale_by(1)

top_roofs = []
for i in range(5):  # Generates building at top of map
    x = gamebox.from_image(100 + i * 280, -1650, 'longroof.png')
    y = gamebox.from_image(100 + i * 280, -1650, 'longroof.png')
    x.rotate(90)
    y.rotate(90)
    top_roofs.append(x)
    top_roofs.append(y)
for roof in top_roofs:
    roof.scale_by(.4)

brick = []
for i in range(4):  # Generates brick at top of map
    wall = gamebox.from_image(50 + i * 250, -1570, 'minecraft_brick.png')
    wall.scale_by(.25)
    brick.append(wall)

for i in range(3):
    path = gamebox.from_image(205 + 205 * i, 100, 'brick.png')
    brick.append(path)
    path2 = gamebox.from_image(205 + 205 * i, -300, 'brick.png')
    brick.append(path2)
    path3 = gamebox.from_image(205 + 205 * i, -800, 'brick.png')
    brick.append(path3)
# walls to set map boundaries
invis_wall = [
    (gamebox.from_color(400, 666, 'red', 800, 20)),
    (gamebox.from_color(-10, 600, 'red', 20, 1600)),
    (gamebox.from_color(810, 600, 'red', 20, 1600)),
    gamebox.from_color(400, -1400, 'red', 800, 20)
]

statue = gamebox.from_image(400, -1200, 'homerstatue.png')  # homer statue used for checkpoint
statue.scale_by(.5)

walking_speed = 9  # player speed
stepcount = 0


################ PLAYER ###################3
def make_player(x, y):
    """
    generates list of player sprites for animation
    :param x: x coordinate
    :param y: y coordinate
    :return: list of player sprites
    """
    global frames, player_down
    images1 = gamebox.load_sprite_sheet("naked_up.png", 1, 4)
    images2 = gamebox.load_sprite_sheet("naked_down.png", 1, 4)
    images3 = gamebox.load_sprite_sheet("naked_left.png", 1, 4)
    images4 = gamebox.load_sprite_sheet("naked_right.png", 1, 4)
    player = []
    for image in images1:
        player.append(gamebox.from_image(x, y, image))
    for image in images2:
        player.append(gamebox.from_image(x, y, image))
    for image in images3:
        player.append(gamebox.from_image(x, y, image))
    for image in images4:
        player.append(gamebox.from_image(x, y, image))
    frames = 4
    for each in player:
        each.scale_by(.15)
    return player


clock = 0
nextFrame = 0
frame = 0


def move_player(player, keys):
    """
    Controls player movement and animation
    :param player: make_player(x,y)
    :param keys: w,a,s,d
    :return: None
    """
    global stepcount, frame, game_on, game_on2, checkpoint, win
    if game_on2:
        if pygame.K_w in keys:  # player up movement
            for i in player:
                i.y -= walking_speed
                i.move_speed()
            stepcount += 0.5
            frame = int(stepcount) % (frames)
            camera.draw(player[frame])
        if pygame.K_s in keys:  # player down movement
            for i in player:
                i.y += walking_speed
                i.move_speed()
            stepcount += 0.5
            frame = int(stepcount) % (frames)
            camera.draw(player[frame + 4])
        if pygame.K_a in keys:  # player left movement
            for i in player:
                i.x -= walking_speed
                i.move_speed()
            stepcount += 0.5
            frame = int(stepcount) % (frames)
            camera.draw(player[frame + 8])
        if pygame.K_d in keys:  # player right movement
            for i in player:
                i.x += walking_speed
                i.move_speed()
            stepcount += 0.5
            frame = int(stepcount) % (frames)
            camera.draw(player[frame + 12])
        if pygame.K_w not in keys and pygame.K_s not in keys and pygame.K_a not in keys and pygame.K_d not in keys:
            camera.draw(player[frame])  # player idle frame
        camera.y = player[0].y  # camera follows player in y direction
        for each in player:
            for wall in invis_wall:
                each.move_to_stop_overlapping(wall)  # player can't go outside of boundaries
        for each in player:
            for roof in roofs:
                each.move_to_stop_overlapping(roof)  # player can't go into buildings on the lawn
        for each in player:
            if each.touches(statue):
                checkpoint = True  # Gives player a checkpoint when touching the homer statue
        for each in player:
            if checkpoint:
                statue_icon = gamebox.from_image(camera.x - 300, camera.y - 250, 'statue_icon.png')
                statue_icon.scale_by(0.05)
                camera.draw(statue_icon)
                # draws an icon in top-left to notify player that they have reached the checkpoint (statue)
                if each.touches(steps):
                    game_on2 = False
                    win = True  # game ends and win is true when player gets back to rotunda
        for each in player:  # ends game when player touches enemies
            for t in trainer:
                if each.touches(t):
                    game_on2 = False
            for t in trainer2:
                if each.touches(t):
                    game_on2 = False

            for s in squirrel:
                if each.touches(s):
                    game_on2 = False
            for s in squirrel2:
                if each.touches(s):
                    game_on2 = False
            for s in squirrel3:
                if each.touches(s):
                    game_on2 = False

            for g in girl:
                if each.touches(g):
                    game_on2 = False
            for g in girl2:
                if each.touches(g):
                    game_on2 = False
            for p in police:
                if each.touches(p):
                    game_on2 = False
            for p in police2:
                if each.touches(p):
                    game_on2 = False


player = make_player(400, 500)


################ ENEMIES ###########################
def make_trainer(x, y):
    """
    creates enemy pokemon trainer sprites
    :param x: x coordinate
    :param y: y coordinate
    :return: trainer and trainer2 lists of sprites
    """
    images1 = gamebox.load_sprite_sheet("player_left.png", 1, 4)
    images2 = gamebox.load_sprite_sheet("player_right.png", 1, 4)
    trainer = []
    for image in images1:
        trainer.append(gamebox.from_image(x, y, image))
    for image in images2:
        trainer.append(gamebox.from_image(x, y, image))
    trainer2 = trainer
    return trainer, trainer2


trainer_speed = 10
trainercount = 0
left = True


def move_trainer(trainer):
    """
    moves trainer sprite
    :param trainer: trainer sprite list
    :return:
    """
    global trainer_speed, trainercount, left
    if left:
        for i in trainer:
            i.x -= trainer_speed
            i.move_speed()
        trainercount += 0.5
        frame = int(trainercount) % frames
        camera.draw(trainer[frame])
    else:
        for i in trainer:
            i.x += trainer_speed
            i.move_speed()
        trainercount += 0.5
        frame = int(trainercount) % frames
        camera.draw(trainer[frame + 4])
    for each in trainer:
        if each.x < 20:
            left = False
        if each.x > 780:
            left = True


left2 = False
trainercount2 = 0


def move_trainer2(trainer2):
    """
    moves trainer2 sprite
    :param trainer2: trainer2 sprite list
    :return:
    """
    global trainer_speed, trainercount2, left2
    if left2:
        for i in trainer2:
            i.x -= trainer_speed
            i.move_speed()
        trainercount2 += 0.5
        frame2 = int(trainercount2) % 4
        camera.draw(trainer2[frame2])
    else:
        for i in trainer2:
            i.x += trainer_speed
            i.move_speed()
        trainercount2 += 0.5
        frame2 = int(trainercount2) % 4
        camera.draw(trainer2[frame2 + 4])
    for each in trainer2:
        if each.x < 20:
            left2 = False
        if each.x > 780:
            left2 = True


############# SQUIRREL ################
def make_squirrel(x, y):
    """
    creates 3 squirrel sprite lists
    :param x: x coordinate
    :param y: y coordinate
    :return: squirrel, squirrel2, squirrel3 sprite lists
    """
    global squirrel_frames
    images1 = gamebox.load_sprite_sheet("squirrel_left.png", 1, 3)
    images2 = gamebox.load_sprite_sheet("squirrel_right.png", 1, 3)
    squirrel = []
    for image in images1:
        squirrel.append(gamebox.from_image(x, y, image))
    for image in images2:
        squirrel.append(gamebox.from_image(x, y, image))
    squirrel2 = squirrel
    squirrel3 = squirrel
    squirrel_frames = 3
    return squirrel, squirrel2, squirrel3


squirrel_frame = 0
squirrel_speed = 20
squirrelcount = 0
squirrel_left = True


def move_squirrel1(squirrel):
    """
    move squirrel enemy
    :param squirrel: squirrel sprite sheet
    :return:
    """
    global squirrel_speed, squirrelcount, squirrel_left
    if squirrel_left:
        for i in squirrel:
            i.x -= squirrel_speed
            i.move_speed()
        squirrelcount += 0.5
        squirrel_frame = int(squirrelcount) % squirrel_frames
        camera.draw(squirrel[squirrel_frame])
    else:
        for i in squirrel:
            i.x += squirrel_speed
            i.move_speed()
        squirrelcount += 0.5
        squirrel_frame = int(squirrelcount) % squirrel_frames
        camera.draw(squirrel[squirrel_frame + 3])
    for each in squirrel:
        if each.x < 20:
            squirrel_left = False
        if each.x > 780:
            squirrel_left = True


squirrel_left2 = True


def move_squirrel2(squirrel2):
    """
    moves squirrel2
    :param squirrel: squirrel sprite list
    :return:
    """
    global squirrel_speed, squirrelcount, squirrel_left2
    if squirrel_left2:
        for i in squirrel2:
            i.x -= squirrel_speed
            i.move_speed()
        squirrelcount += 0.5
        squirrel_frame = int(squirrelcount) % squirrel_frames
        camera.draw(squirrel2[squirrel_frame])
    else:
        for i in squirrel2:
            i.x += squirrel_speed
            i.move_speed()
        squirrelcount += 0.5
        squirrel_frame = int(squirrelcount) % squirrel_frames
        camera.draw(squirrel2[squirrel_frame + 3])
    for each in squirrel2:
        if each.x < 20:
            squirrel_left2 = False
        if each.x > 780:
            squirrel_left2 = True


squirrel_left3 = False


def move_squirrel3(squirrel3):
    """
    moves squirrel3
    :param squirrel3: squirrel 3 sprite list
    :return:
    """
    global squirrel_speed, squirrelcount, squirrel_left3
    if squirrel_left3:
        for i in squirrel3:
            i.x -= squirrel_speed
            i.move_speed()
        squirrelcount += 0.5
        squirrel_frame = int(squirrelcount) % squirrel_frames
        camera.draw(squirrel3[squirrel_frame])
    else:
        for i in squirrel3:
            i.x += squirrel_speed
            i.move_speed()
        squirrelcount += 0.5
        squirrel_frame = int(squirrelcount) % squirrel_frames
        camera.draw(squirrel3[squirrel_frame + 3])
    for each in squirrel3:
        if each.x < 20:
            squirrel_left3 = False
        if each.x > 780:
            squirrel_left3 = True


############ Girl Enemy ##############
def make_girl(x, y):
    """
    creates girl sprite lists
    :param x: x coordinate
    :param y: y coordinate
    :return: girl and girl2 sprite lists
    """
    global girl_frames
    images1 = gamebox.load_sprite_sheet("girl_left.png", 1, 3)
    images2 = gamebox.load_sprite_sheet("girl_right.png", 1, 3)
    girl = []
    for image in images1:
        girl.append(gamebox.from_image(x, y, image))
    for image in images2:
        girl.append(gamebox.from_image(x, y, image))
    for each in girl:
        each.scale_by(.5)
    girl2 = girl
    girl_frames = 3
    return girl, girl2


girl_left = False
girlcount = 0


def move_girl(girl):
    """
    moves girl sprite list
    :param girl: girl sprite list
    :return:
    """
    global trainer_speed, girlcount, girl_left
    if girl_left:
        for i in girl:
            i.x -= trainer_speed
            i.move_speed()
        girlcount += 0.5
        girl_frame = int(girlcount) % 3
        camera.draw(girl[girl_frame])
    else:
        for i in girl:
            i.x += trainer_speed
            i.move_speed()
        girlcount += 0.5
        girl_frame = int(girlcount) % 3
        camera.draw(girl[girl_frame + 3])
    for each in girl:
        if each.x < 20:
            girl_left = False
        if each.x > 780:
            girl_left = True


girl_left2 = True
girlcount2 = 0


def move_girl2(girl):
    """
    moves girl2 sprite list
    :param girl: girl2 sprite list
    :return:
    """
    global trainer_speed, girlcount2, girl_left2
    if girl_left2:
        for i in girl:
            i.x -= trainer_speed
            i.move_speed()
        girlcount2 += 0.5
        girl_frame = int(girlcount2) % 3
        camera.draw(girl[girl_frame])
    else:
        for i in girl:
            i.x += trainer_speed
            i.move_speed()
        girlcount2 += 0.5
        girl_frame = int(girlcount2) % 3
        camera.draw(girl[girl_frame + 3])
    for each in girl:
        if each.x < 20:
            girl_left2 = False
        if each.x > 780:
            girl_left2 = True


############## Police enemy ###############
def make_police(x, y):
    """
    creates police sprite sheets
    :param x: x coordinate
    :param y: y coordinate
    :return: police and police2 sprite lists
    """
    global police_frames
    images1 = gamebox.load_sprite_sheet("police_left.png", 1, 4)
    images2 = gamebox.load_sprite_sheet("police_right.png", 1, 4)
    police = []
    for image in images1:
        police.append(gamebox.from_image(x, y, image))
    for image in images2:
        police.append(gamebox.from_image(x, y, image))
    for each in police:
        each.scale_by(.25)
    police2 = police
    police_frames = 4
    return police, police2


policecount = 0
police_left = True


def move_police(police):
    """
    moves police enemy
    :param police: police sprite list
    :return:
    """
    global trainer_speed, policecount, police_left
    if police_left:
        for i in police:
            i.x -= trainer_speed
            i.move_speed()
        policecount += 0.5
        frame = int(policecount) % frames
        camera.draw(police[frame])
    else:
        for i in police:
            i.x += trainer_speed
            i.move_speed()
        policecount += 0.5
        frame = int(policecount) % frames
        camera.draw(police[frame + 4])
    for each in police:
        if each.x < 20:
            police_left = False
        if each.x > 780:
            police_left = True


policecount2 = 0
police_left2 = True


def move_police2(police):
    """
    moves police2 enemy
    :param police: police2 sprite list
    :return:
    """
    global trainer_speed, policecount2, police_left2
    if police_left2:
        for i in police:
            i.x -= trainer_speed
            i.move_speed()
        policecount2 += 0.5
        frame = int(policecount2) % 4
        camera.draw(police[frame])
    else:
        for i in police:
            i.x += trainer_speed
            i.move_speed()
        policecount2 += 0.5
        frame = int(policecount2) % 4
        camera.draw(police[frame + 4])

    for each in police:
        if each.x < 20:
            police_left2 = False
        if each.x > 780:
            police_left2 = True


############## Enemy Locations ###################
trainer = make_trainer(random.randint(30, 770), random.randint(-900, -800))[0]
trainer2 = make_trainer(random.randint(30, 770), random.randint(100, 300))[1]
squirrel = make_squirrel(random.randint(30, 770), random.randint(-300, 0))[0]
squirrel2 = make_squirrel(random.randint(30, 770), random.randint(-800, -400))[1]
squirrel3 = make_squirrel(random.randint(30, 770), random.randint(-800, -400))[2]
girl = make_girl(random.randint(30, 770), random.randint(-800, -400))[0]
girl2 = make_girl(random.randint(30, 770), random.randint(100, 300))[1]
police = make_police(random.randint(30, 770), random.randint(-350, 100))[0]
police2 = make_police(random.randint(30, 770), random.randint(-1200, -1000))[1]

############ SCORE ###############
score = 0
score2 = 10000000000000
hi_score = 1000000000000000


def draw_score():
    """
    Shows score and high score on screen
    :return: None
    """
    global score, hi_score, score2, win
    if game_on2:
        score2 += 1 / 30
        score2 = round(score2, 3)
        # if score % 30 == 0:
        #     score2 += 1
    camera.draw("Time: " + str(score2), 30, "black", camera.x + 250, 30)
    if hi_score < 1000000000000000:
        camera.draw('Hi ' + str(hi_score), 30, "black", camera.x + 150, 30)
    if win:
        draw_hi_score()


def draw_hi_score():
    """
    Updates high score
    :return: None
    """
    global score2, hi_score
    if score2 < hi_score:
        hi_score = score2


########### RESET GAME ###############3
def reset():
    """
    Resets Game
    :return: None
    """
    global score2, checkpoint, win, trainer2, trainer
    global squirrel, squirrel2, squirrel3
    global girl, girl2, police, police2
    score2 = 0
    checkpoint = False
    win = False
    trainer = make_trainer(random.randint(30, 770), random.randint(100, 250))[0]
    trainer2 = make_trainer(random.randint(30, 770), random.randint(-900, -700))[1]
    squirrel = make_squirrel(random.randint(30, 770), random.randint(-300, 0))[0]
    squirrel2 = make_squirrel(random.randint(30, 770), random.randint(-900, -600))[1]
    squirrel3 = make_squirrel(random.randint(30, 770), random.randint(-800, -400))[2]
    girl = make_girl(random.randint(30, 770), random.randint(-800, -400))[0]
    girl2 = make_girl(random.randint(30, 770), random.randint(0, 200))[1]
    police = make_police(random.randint(30, 770), random.randint(-350, 100))[0]
    police2 = make_police(random.randint(30, 770), random.randint(-1200, -1000))[1]


################ KEYS ###################
def tick(keys):
    """
    This function loops through the program by calling on functions
    :param keys: a,s,d,w,space
    :return:
    """
    global game_on, game_on2, frame, clock, nextFrame, player, win, checkpoint
    camera.clear('black')
    start = gamebox.from_image(camera.x, camera.y, 'start_screen.png')
    if not game_on2:
        if pygame.K_SPACE in keys:
            game_on = True
            game_on2 = True
            reset()
    if not game_on2:
        player = make_player(400, 500)
        end_screen = gamebox.from_image(camera.x, camera.y, 'score_display.png')
        camera.draw(end_screen)
        final_score = gamebox.from_text(camera.x, camera.y + 50, str(score2) + " Seconds", 66, 'white')
        camera.draw(final_score)
    if win:
        win_screen = gamebox.from_image(camera.x, camera.y, 'win_screen.png')
        camera.draw(win_screen)
        final_score = gamebox.from_text(camera.x, camera.y + 20, str(score2) + " Seconds", 66, 'white')
        camera.draw(final_score)
        high_score_text = gamebox.from_text(camera.x, camera.y + 100, "High Score:", 66, 'white')
        camera.draw(high_score_text)
        high_score = gamebox.from_text(camera.x, camera.y + 150, str(hi_score) + " Seconds", 66, 'white')
        camera.draw(high_score)
    if game_on2 == True:
        for wall in invis_wall:
            camera.draw(wall)
        for patch in grass:
            camera.draw(patch)
        camera.draw(statue)
        camera.draw(steps)
        for wall in brick:
            camera.draw(wall)
        for roof in top_roofs:
            camera.draw(roof)
        move_player(player, keys)
        move_trainer(trainer)
        move_trainer2(trainer2)
        move_squirrel1(squirrel)
        move_squirrel2(squirrel2)
        move_squirrel3(squirrel3)
        move_girl(girl)
        move_girl2(girl2)
        move_police(police)
        move_police2(police2)
        for roof in roofs:
            camera.draw(roof)
        draw_score()
    if not game_on:
        camera.draw(start)

    camera.display()


gamebox.timer_loop(30, tick)