from tkinter import *
import random
import os

GAME_WIDTH = 1000
GAME_HEIGHT = 500
SPEED = 100  # kecepatan ular semakin rendah semakin cepat
SPACE_SIZE = 50  # ukuran objek di dalam game
BODY_PARTS = 3  # bagian tubuh ular
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FFFF00"
OBSTACLE_COLOR = "#FF0000"  # warna obstacle
BACKGROUND_COLOR = "#808080"
HIGH_SCORE_FILE = "high_score.txt"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

class Obstacle:
    def __init__(self):
        self.coordinates = [
            (GAME_WIDTH // 4, GAME_HEIGHT // 2),
            (GAME_WIDTH // 2, GAME_HEIGHT // 2),
            (3 * GAME_WIDTH // 4, GAME_HEIGHT // 2)
        ]

        for x, y in self.coordinates:
            canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")

def next_turn(snake, food):
    global obstacle  # ensure obstacle is accessible
    
    if is_auto_mode:
        auto_chase_food(snake, food)
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score: {}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def auto_chase_food(snake, food):
    global direction
    
    head_x, head_y = snake.coordinates[0]
    food_x, food_y = food.coordinates

    if head_x < food_x and direction != "left":
        direction = "right"
    elif head_x > food_x and direction != "right":
        direction = "left"
    elif head_y < food_y and direction != "up":
        direction = "down"
    elif head_y > food_y and direction != "down":
        direction = "up"

def change_direction(new_direction):
    global direction

    if not is_auto_mode:
        if new_direction == 'left' and direction != 'right':
            direction = new_direction
        elif new_direction == 'right' and direction != 'left':
            direction = new_direction
        elif new_direction == 'up' and direction != 'down':
            direction = new_direction
        elif new_direction == 'down' and direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    for obstacle_coord in obstacle.coordinates:
        if x == obstacle_coord[0] and y == obstacle_coord[1]:
            return True
        
    return False

def game_over():
    global high_score
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('Times New Roman', 70), text="GAME OVER", fill="red", tag="gameover")
    
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(high_score))
        high_score_label.config(text="High Score: {}".format(high_score))
    
def restart_game():
    global snake, food, score, direction, obstacle

    # Reset game variables to initial values
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    obstacle = Obstacle()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)

def toggle_mode():
    global is_auto_mode
    is_auto_mode = not is_auto_mode
    mode_button.config(text="Mode: Auto" if is_auto_mode else "Mode: Manual")

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

window = Tk()
window.title("Snake Game")
window.resizable(False, False) # mengubah ukuran windows

score = 0
high_score = load_high_score()
direction = 'down'
is_auto_mode = False

label = Label(window, text="Score: {}".format(score), font=('Times New Roman', 20))
label.pack()

high_score_label = Label(window, text="High Score: {}".format(high_score), font=('Times New Roman', 20))
high_score_label.pack()

restart_button = Button(window, text="Restart", command=restart_game, font=('Times New Roman', 20))
restart_button.place(x=0, y=0)

frame = Frame(window)
frame.pack(pady=10)  # Menambahkan padding di antara frame dan label skor

canvas = Canvas(frame, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

mode_button = Button(frame, text="Mode: Manual", command=toggle_mode, font=('Times New Roman', 10))
mode_button.pack(pady=12)  # Menambahkan padding antara kanvas dan tombol mode

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()
obstacle = Obstacle()

next_turn(snake, food)

window.mainloop()
