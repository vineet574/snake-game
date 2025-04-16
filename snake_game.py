import pygame
import time
import random
import requests

pygame.init()

width = 600
height = 400

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

block_size = 10
speed = 15

font = pygame.font.SysFont("bahnschrift", 25)
headline_font = pygame.font.SysFont("comicsansms", 15)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with News Headlines")

clock = pygame.time.Clock()

def fetch_headlines():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    headlines = [article["title"] for article in articles if "title" in article]
    return headlines

def draw_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, black, [x[0], x[1], block_size, block_size])

def display_score(score):
    value = font.render("Score: " + str(score), True, white)
    window.blit(value, [10, 10])

def game():
    game_over = False
    game_close = False

    x = width / 2
    y = height / 2

    dx = 0
    dy = 0

    snake_list = []
    length = 1

    food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0

    headlines = fetch_headlines()
    current_headline = random.choice(headlines) if headlines else "No headlines available"

    while not game_over:

        while game_close:
            window.fill(blue)
            message = font.render("You Lost! Press Q-Quit or C-Play Again", True, red)
            window.blit(message, [width / 6, height / 3])
            display_score(length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -block_size
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = block_size
                    dx = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += dx
        y += dy
        window.fill(blue)
        pygame.draw.rect(window, green, [food_x, food_y, block_size, block_size])
        
        snake_head = [x, y]
        snake_list.append(snake_head)
        
        if len(snake_list) > length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(block_size, snake_list)
        display_score(length - 1)

        headline_text = headline_font.render(current_headline, True, white)
        window.blit(headline_text, [10, height - 30])
        
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            length += 1
            current_headline = random.choice(headlines) if headlines else "No headlines available"

        clock.tick(speed)

    pygame.quit()
    quit()

game()
