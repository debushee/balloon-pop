# Import
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import pygame_textinput
import SendToDb

# Initialize
pygame.init()

# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Popping")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# Images
imgBalloon = pygame.image.load('./Resources/BalloonRed.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 500, 300

# Variables
speed = 15
score = 0
startTime = time.time()
totalTime = 60

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Database setup
SendToDb.CreateTableResults()

# Basic font for user typed
base_font = pygame.font.Font(None, 32)
# Fonts
smallfont = pygame.font.SysFont('Corbel', 20)
bigfont = pygame.font.SysFont('Corbel', 40)
user_text = ''

# create rectangle for Welcome message
welcome_rect = pygame.Rect(20, 20, 650, 50)
# create rectangle for tips message
tips_rect = pygame.Rect(20, 100, 650, 32)
# create rectangle for Enter Name
enter_name_rect = pygame.Rect(20, 150, 200, 32)
# Create TextInput object
text_input = pygame_textinput.TextInputVisualizer()
text_input.font_color = pygame.Color('white')
text_input.cursor_color = pygame.Color('white')
text_input.value = ''
# create rectangle for submit button
submit_rect = pygame.Rect(20, 200, 140, 32)

# color_active stores color(lightskyblue3) which gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')
# color of input box
color_passive = pygame.Color('chartreuse4')
color = color_passive
welcome_active = True
start_game = False
enterNameText = ''
# Get mouse position
mouse = pygame.mouse.get_pos()


def welcome_loop():
    welcome_active = True
    user_text = ''
    text_input.value = ''
    while welcome_active:
        events = pygame.event.get()
        # Feed it with events every frame
        text_input.update(events)
        for event in events:
            # if user clicks QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_rect.collidepoint(event.pos):
                    welcome_active = False
                    return welcome_active, text_input.value

            if event.type == pygame.KEYDOWN:
                # check for enter/return key
                if event.type == pygame.K_RETURN:
                    welcome_active = False
                    return welcome_active, text_input.value
        # set background color of screen
        window.fill((22, 28, 34))

        # draw rectangle and argument passed
        pygame.draw.rect(window, color_passive, welcome_rect)
        pygame.draw.rect(window, color_passive, tips_rect)
        pygame.draw.rect(window, color_passive, enter_name_rect)
        pygame.draw.rect(window, color_passive, submit_rect, 0, 6)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render
        welcomeText = bigfont.render('Welcome to Balloon Pop!', True, "white")
        tipsText = smallfont.render(
            'Burst as many balloons as you can in 60 seconds!', True, "white")
        enterNameText = smallfont.render(
            'Please enter your name:', True, "white")
        submitText = smallfont.render('Play', True, "white")
        window.blit(welcomeText, (25, 25))
        window.blit(tipsText, (25, 105))
        window.blit(enterNameText, (25, 155))
        window.blit(submitText, (25, 205))
        window.blit(text_input.surface, (240, 155))

        # display.flip() will update only a portion of the screen to updated, not full area
        pygame.display.flip()
        pygame.display.update()

        # clock.tick(60) means that for every second at most 60 frames should be passed.
        clock.tick(60)


def main_game_loop(user_text):
    # Main loop
    start_game = True
    sentToDb = False
    # Set variables
    speed = 10
    score = 0
    startTime = time.time()
    totalTime = 60

    while start_game:
        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_game = False
                pygame.quit()

        # Apply Logic
        timeRemain = int(totalTime - (time.time()-startTime))
        if timeRemain < 0:
            # Set background color of screen
            window.fill((22, 28, 34))
            font = pygame.font.Font('./Resources/Marcellus-Regular.ttf', 40)
            textScore = font.render(
                f'Your Score: {score}', True, color_passive)
            yourName = font.render(
                f'Well done {user_text}', True, color_passive)
            window.blit(textScore, (450, 50))
            window.blit(yourName, (450, 10))

            # Create rectangle for Next player button
            next_player_rect = pygame.Rect(420, 600, 150, 40)
            pygame.draw.rect(window, color_passive, next_player_rect, 0, 6)
            nextPlayer = smallfont.render(f'Next player', True, 'white')
            window.blit(nextPlayer, (440, 610))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_player_rect.collidepoint(event.pos):
                    start_game = False
                    return start_game
                else:
                    start_game = True

            column_space = 50
            head1 = font.render(f'RANK', True, color_passive)
            head2 = font.render(f'PLAYER', True, color_passive)
            head3 = font.render(f'SCORE', True, color_passive)
            window.blit(head1, (150, 150))
            window.blit(head2, (450, 150))
            window.blit(head3, (800, 150))
            i = 35
            rows = SendToDb.leader_board()
            rank = 1
            for row in rows:
                column1 = font.render(f'{rank}', True, color_passive)
                column2 = font.render('{:>3}'.format(
                    row[1]), True, color_passive)
                column3 = font.render('{:30}'.format(
                    row[2]), True, color_passive)
                window.blit(column1, [150, (700 / 4) + i + 5])
                window.blit(column2, [450, (700 / 4) + i + 5])
                window.blit(column3, [450 + column_space, (700 / 4) + i + 5])
                i += 35
                rank += 1
            if sentToDb == False:
                SendToDb.AddResult(user_text, score)
                sentToDb = True

        else:
            # OpenCV
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)

            rectBalloon.y -= speed  # Move the balloon up
            # check if balloon has reached the top without a pop
            if rectBalloon.y < 0:
                rectBalloon.x = random.randint(100, img.shape[1] - 100)
                rectBalloon.y = img.shape[0] + 50
                speed += 1

            if hands:
                hand = hands[0]
                x, y = hand['lmList'][8][0:2]
                if rectBalloon.collidepoint(x, y):
                    rectBalloon.x = random.randint(100, img.shape[1] - 100)
                    rectBalloon.y = img.shape[0] + 50
                    score += 10
                    speed += 1

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(imgBalloon, rectBalloon)

            font = pygame.font.Font('./Resources/Marcellus-Regular.ttf', 50)
            textScore = font.render(f'Score: {score}', True, (50, 50, 255))
            textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
            window.blit(textScore, (35, 35))
            window.blit(textTime, (1000, 35))

        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)


# Main game loop
main_game_flag = True
while main_game_loop:
    if welcome_active:
        welcome_active, user_text = welcome_loop()
    else:
        start_game = main_game_loop(user_text)
        if start_game == False:
            welcome_active = True
