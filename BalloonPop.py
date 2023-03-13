# Import
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import SendToDb


# Initialize
pygame.init()

# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cloud Bursting")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# Images
imgBalloon = pygame.image.load('./Resources/cloud-ready2.png').convert_alpha()
# imgBalloon = pygame.image.load('./Resources/BalloonRed.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 500, 300



# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


def resetBalloon():
    rectBalloon.x = random.randint(100, img.shape[1] - 100)
    rectBalloon.y = img.shape[0] + 50

  
# basic font for user typed
base_font = pygame.font.Font(None, 32)
user_text = ''

# create rectangle for Welcome message
welcome_rect = pygame.Rect(20, 20, 650, 50)
# create rectangle for tips message
tips_rect = pygame.Rect(20, 100, 650, 32)
# create rectangle for Enter Name
enter_name_rect = pygame.Rect(20, 150, 200, 32)
# create rectangle for user input
input_rect = pygame.Rect(230, 150, 140, 32)
# create rectangle for submit button
submit_rect = pygame.Rect(20, 200, 140, 32)

# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')
  
# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = True
enterNameText = ''
# Get mouse position
mouse = pygame.mouse.get_pos()
while active:
    for event in pygame.event.get():
  
      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.MOUSEBUTTONDOWN:
              if 20 <= mouse[0] <= 160 and 150 <= mouse[1] <= 182:
                    active = False

        if event.type == pygame.KEYDOWN:
  
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
  
                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]
  
            # Unicode standard is used for string
            # formation
            else:
                user_text += event.unicode

    # it will set background color of screen
    window.fill((22, 28, 34))
  
    if active:
        color = color_active
    else:
        color = color_passive
          
    # draw rectangle and argument passed which should
    # be on screen
    pygame.draw.rect(window, color_passive, welcome_rect)
    pygame.draw.rect(window, color_passive, tips_rect)
    pygame.draw.rect(window, color_passive, enter_name_rect)
    pygame.draw.rect(window, color, input_rect)
    pygame.draw.rect(window, color_passive, submit_rect,0,6)
  
    text_surface = base_font.render(user_text, True, (255, 255, 255))
      
    # render at position stated in arguments
    window.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    smallfont = pygame.font.SysFont('Corbel',20)
    bigfont = pygame.font.SysFont('Corbel',40)
    welcomeText = bigfont.render('Welcome to the Cloud Bursting game!' , True , "white")
    tipsText = smallfont.render('Burst as many clouds as you can in 60 seconds...using your fingers' , True , "white")
    enterNameText = smallfont.render('Please enter your name:' , True , "white")
    submitText = smallfont.render('Play' , True , "white")
    window.blit(welcomeText , (25 , 25))
    window.blit(tipsText , (25 , 105))
    window.blit(enterNameText , (25 , 155))
    window.blit(submitText , (25 , 205))
      
    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, text_surface.get_width()+10)
      
    # display.flip() will update only a portion of the
    # screen to updated, not full area
    pygame.display.flip()
      
    # clock.tick(60) means that for every second at most
    # 60 frames should be passed.
    clock.tick(60)


# # Main loop
start = True
sentToDb = False
# Variables
speed = 15
score = 0
startTime = time.time()
totalTime = 60
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    timeRemain = int(totalTime -(time.time()-startTime))
    if timeRemain <0:
        window.fill((255,255,255))

        font = pygame.font.Font('./Resources/Marcellus-Regular.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time UP', True, (50, 50, 255))
        yourName = font.render(user_text, True, (50, 50, 255))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (450, 275))
        window.blit(yourName, (450, 200))
        if sentToDb == False:
            SendToDb.SendToDb(user_text, score)
            sentToDb = True
    else:
        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        rectBalloon.y -= speed  # Move the balloon up
        # check if balloon has reached the top without pop
        if rectBalloon.y < 0:
            resetBalloon()
            speed += 1

        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8][0:2]
            if rectBalloon.collidepoint(x, y):
                resetBalloon()
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

# print(user_text)
# print(textScore)