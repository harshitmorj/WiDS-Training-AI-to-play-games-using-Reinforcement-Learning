import pygame
from pygame.locals import *
from random import randint


class Snake(pygame.sprite.Sprite):
    def __init__(self, head):
        super(Snake, self).__init__()
        self.headsq = head
        self.tailsq = head
        self.body = [head, ]
        self.size = 1


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super(Square, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 212, 59))
        self.pos = [x, y]
        self.dir = dir  # 0 is up, 1 is right and so on


def bodycollide(snake):
    if (snake.headsq.pos in [i.pos for i in snake.body[:-1]]):
        return 1


def gameover(snake):
    if (780 < snake.headsq.pos[0] or snake.headsq.pos[0] < 0) or (580 < snake.headsq.pos[1] or snake.headsq.pos[1] < 0) or bodycollide(snake):
        print("Game Over")
        print("Your Score:", snake.size - 1)
        return 1
    return 0


def erasetail(snake):
    snake.body[0].surf.fill((0, 0, 0))
    screen.blit(snake.body[0].surf, tuple(snake.body[0].pos))


def changedir(snake, keys):
    if (keys[K_w] or keys[K_UP]) and snake.headsq.dir != 2:
        snake.headsq.dir = 0
    elif (keys[K_a] or keys[K_LEFT]) and snake.headsq.dir != 1:
        snake.headsq.dir = 3
    elif (keys[K_s] or keys[K_DOWN]) and snake.headsq.dir != 0:
        snake.headsq.dir = 2
    elif (keys[K_d] or keys[K_RIGHT]) and snake.headsq.dir != 3:
        snake.headsq.dir = 1


def drawhead(snake):
    snake.body[-1].surf.fill((255, 212, 59))
    screen.blit(snake.body[-1].surf, tuple(snake.body[-1].pos))


def updatesnake(snake):
    for i in range(snake.size-1):
        snake.body[i].pos[0] = snake.body[i+1].pos[0]
        snake.body[i].pos[1] = snake.body[i+1].pos[1]

    if (snake.headsq.dir == 0):
        snake.headsq.pos[1] -= 20
    if (snake.headsq.dir == 1):
        snake.headsq.pos[0] += 20
    if (snake.headsq.dir == 2):
        snake.headsq.pos[1] += 20
    if (snake.headsq.dir == 3):
        snake.headsq.pos[0] -= 20


# food on screen or not
f = fx = fy = 0


def food(snake):
    global f, fx, fy
    if (f == 0):
        fx = randint(0, 800)//20*20
        fy = randint(0, 600)//20*20

        food = pygame.Surface((20, 20))
        food.fill((48, 105, 152))
        screen.blit(food, (fx, fy))
        f = 1

    if (snake.headsq.pos == [fx, fy] and f == 1):
        snake.headsq = Square(fx, fy, snake.headsq.dir)
        snake.size += 1
        snake.body += [snake.headsq, ]
        f = 0


pygame.init()

screen = pygame.display.set_mode((800, 600))

snake = Snake(Square(40, 40, 1))


# Use blit to put something on the screen
screen.blit(snake.headsq.surf, tuple(snake.headsq.pos))

# Update the display using flip
pygame.display.flip()

gameOn = 1
# Our game loop
while gameOn:
    # for loop through the event queue
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = 0
    keys = pygame.key.get_pressed()

    erasetail(snake)

    changedir(snake, keys)

    food(snake)

    updatesnake(snake)

    drawhead(snake)

    # Update the display using flip
    pygame.display.flip()
    pygame.time.delay(int(200*1/(snake.size/10 + 1)))

    if gameover(snake):
        gameOn = 0

pygame.quit()
