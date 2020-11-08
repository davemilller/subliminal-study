import random
import smtplib
import ssl
from email.mime.text import MIMEText

import pygame

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
width = 800
height = 600

xyR = (550, 250)
xyL = (150, 250)
fixPos = (375, 275)
circlePrime = pygame.image.load('circle-small.png')
leftArrow = pygame.image.load('circle.png')
rightArrow = pygame.image.load('circle.png')
fixation = pygame.image.load('fixation2.png')

right = 'pygame.K_RIGHT'
left = 'pygame.K_LEFT'

results = {"compatible": [], "incompatible": [], "no-prime": [], "long-prime-compatible": [],
           "long-prime-incompatible": []}

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((width / 2), (height / 4))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    pygame.time.delay(2000)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


# send results to an email for easy gathering purposes
def sendResults():
    port = 465
    password = 'KXgj64gxDF4nSJE'
    context = ssl.create_default_context()
    message = str(results)
    message = MIMEText(message, 'plain')
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("subliminal.study@gmail.com", password)
        server.sendmail("subliminal.study@gmail.com", "subliminal.study@gmail.com", message.as_string())


def prime():
    n = random.randint(1, 2)
    if n == 1:
        t = right
        screen.blit(circlePrime, (575, 275))
    else:
        t = left
        screen.blit(circlePrime, (125, 275))
    return t


# give 20% chance for target and prime to be dif directions
def target(primeD):
    n = random.randint(1, 5)
    if n == 2:
        if primeD == left:
            t = right
            screen.blit(rightArrow, xyR)
        else:
            t = left
            screen.blit(leftArrow, xyL)
    else:
        if primeD == left:
            t = left
            screen.blit(leftArrow, xyL)
        else:
            t = right
            screen.blit(rightArrow, xyR)
    return t


def titleScreen():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(results)
                sendResults()
                quit(0)

        screen.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Subthreshold Perception", largeText)
        TextRect.center = ((width / 2), (height / 3))
        screen.blit(TextSurf, TextRect)
        button("Play", 325, 450, 150, 50, green, green, play)
        pygame.display.update()
        clock.tick(15)


def play():
    count = 0

    # main loop
    while count < 50:
        # blended trial
        n = random.randint(1, 5)
        if n == 1 or n == 2: # short-prime
            primeTime = 20
            trial = 'short-prime'
        elif n == 3:    # no-prime
            primeTime = 0
            trial = 'no-prime'
        else:           # long-prime
            primeTime = 50
            trial = 'long-prime'

        screen.fill(white)
        screen.blit(fixation, fixPos)
        pygame.display.update()
        pygame.time.wait(1000)

        # prime
        primeDir = prime()
        pygame.display.update()

        # show prime based on trial type
        pygame.time.delay(primeTime)

        # white for 350 ms
        screen.fill(white)
        screen.blit(fixation, fixPos)
        pygame.display.update()

        pygame.time.wait(350)
        pygame.event.clear()

        # target for 2 sec, get difference in time from here to key press (response time)
        targetDir = target(primeDir)
        clock.tick_busy_loop()
        pygame.display.update()

        pressed = pygame.event.wait()

        clock.tick_busy_loop()
        pygame.time.delay(2000)

        # difference between t1 and t2
        response_time = clock.get_time()
        print(response_time)

        # fill results dict
        if trial == 'short-prime':
            if targetDir == primeDir:
                results["compatible"].append(response_time)
            else:
                results["incompatible"].append(response_time)
        elif trial == 'no-prime':
            results['no-prime'].append(response_time)
        else:
            if targetDir == primeDir:
                results["long-prime-compatible"].append(response_time)
            else:
                results["long-prime-incompatible"].append(response_time)

        if pressed.type == pygame.QUIT:
            pygame.quit()
            print(results)
            sendResults()
            exit(0)

        count += 1
        pygame.time.delay(1000)


titleScreen()
