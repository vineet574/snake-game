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

font = pygame.font.SysFont("bahnschrift", 25)
headline_font = pygame.font.SysFont("comicsansms", 15)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with News Headlines")

clock = pygame.time.Clock()

# Load sounds if mixer initialized
eat_sound = None
game_over_sound = None
if pygame.mixer.get_init():
    try:
        eat_sound = pygame.mixer.Sound('eat.wav')
        game_over_sound = pygame.mixer.Sound('gameover.wav')
    except:
        pass

def fetch_headlines():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        articles = data.get("articles", [])
        headlines = [article["title"] for article in articles if "title" in article]
        return headlines if headlines else ["No headlines available"]
    except:
        return ["Unable to fetch news"]

def draw_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, black, [x[0], x[1], block_size, block_size])

def display_score(score):
    value = font.render("Score: " + str(score), True, white)
    window.blit(value, [10, 10])

def display_timer(start_time):
    elapsed_time = int(time.time() - start_time)
    timer_surface = font.render(f"Time: {elapsed_time}s", True, white)
    window.blit(timer_surface, [width - 140, 10])

def display_best_score(best_score):
    best_score_surface = font.render(f"Best: {best_score}", True, white)
    window.blit(best_score_surface, [width // 2 - 40, 10])

def display_headlines(headlines, offset):
    y_pos = height - 30
    x_pos = -offset
    space = 50
    for headline in headlines:
        text_surface = headline_font.render(headline, True, white)
        window.blit(text_surface, (x_pos, y_pos))
        x_pos += text_surface.get_width() + space

def load_best_score():
    try:
        with open("best_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_best_score(score):
    try:
        with open("best_score.txt", "w") as f:
            f.write(str(score))
    except:
        pass

def select_difficulty():
    selecting = True
    selected_speed = None
    while selecting:
        window.fill(blue)
        title = font.render("Select Difficulty: 1-Easy 2-Medium 3-Hard", True, white)
        window.blit(title, (width // 10, height // 3))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_speed = 10
                    selecting = False
                elif event.key == pygame.K_2:
                    selected_speed = 15
                    selecting = False
                elif event.key == pygame.K_3:
                    selected_speed = 25
                    selecting = False
    return selected_speed

def game():
    global block_size
    speed = select_difficulty()
    game_over = False
    game_close = False
    paused = False

    x = width / 2
    y = height / 2

    dx = 0
    dy = 0

    snake_list = []
    length = 1

    food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0

    headlines = fetch_headlines()
    headlines_to_scroll = headlines * 3

    start_time = time.time()
    best_score = load_best_score()
    scroll_offset = 0
    scroll_speed = 2
    flicker = False
    flicker_timer = 0

    while not game_over:

        while game_close:
            if pygame.mixer.get_init() and game_over_sound:
                game_over_sound.play()
            window.fill(blue)
            elapsed_time = int(time.time() - start_time)
            if flicker:
                message = font.render("You Lost! Press Q-Quit or C-Play Again", True, red)
            else:
                message = font.render("You Lost! Press Q-Quit or C-Play Again", True, white)
            flicker_timer += 1
            if flicker_timer > 10:
                flicker = not flicker
                flicker_timer = 0
            score_text = font.render(f"Final Score: {length - 1}", True, white)
            time_text = font.render(f"Time Survived: {elapsed_time}s", True, white)
            window.blit(message, [width / 6, height / 3])
            window.blit(score_text, [width / 3, height / 2])
            window.blit(time_text, [width / 3, height / 2 + 30])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -block_size
                        dy = 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = block_size
                        dy = 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dy = -block_size
                        dx = 0
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dy = block_size
                        dx = 0

        if paused:
            window.fill(blue)
            pause_text = font.render("Paused. Press P to Resume.", True, white)
            window.blit(pause_text, [width // 4, height // 2])
            pygame.display.update()
            clock.tick(5)
            continue

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
        display_best_score(best_score)
        display_timer(start_time)

        scroll_offset += scroll_speed
        total_width = sum(headline_font.size(h)[0] + 50 for h in headlines_to_scroll)
        if scroll_offset > total_width:
            scroll_offset = 0
        display_headlines(headlines_to_scroll, scroll_offset)

        pygame.display.update()

        if x == food_x and y == food_y:
            if pygame.mixer.get_init() and eat_sound:
                eat_sound.play()
            food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            length += 1
            if length - 1 > best_score:
                best_score = length - 1
                save_best_score(best_score)

        clock.tick(speed)

    pygame.quit()
    quit()

game()
