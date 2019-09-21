from tkinter import *
import random
import time


class GameData:
    """
    Game data, configuration and stuff.
    """
    def __init__(self):
        self.name = "Bouncing Ball"
        self.width = 600
        self.height = 600
        self.game_speed = 0.01
        self.start_game = False
        self.score = 0

    def add_score(self, value):
        self.score += value
        print("Your score: " + str(self.score))

    def hit_space(self, evt):
        """
        At the begining to start a game with SPACE button.

        :param evt:
        :return:
        """

        if not self.start_game:
            self.start_game = True

    def set_speed(self, speed):
        """
        Game speed configuration.

        :param speed: game speed
        :return:
        """
        self.game_speed = speed

##########################################
#         Game window definition         #
##########################################


config = GameData()
game_app = Tk()
game_app.title(config.name)
game_app.resizable(0, 0)
game_app.wm_attributes("-topmost", 1)

canvas = Canvas(game_app, width=config.width, height=config.height, bd=0, highlightthickness=0, background='black')
canvas.pack()
game_app.update()

canvas.bind_all("<space>", config.hit_space)

main_menu = Menu()
speed_menu = Menu(main_menu)
main_menu.add_cascade(label="Speed", menu=speed_menu)
speed_menu.add_command(label="Low", command=lambda: config.set_speed(0.03))
speed_menu.add_command(label="Medium", command=lambda: config.set_speed(0.02))
speed_menu.add_command(label="Fast", command=lambda: config.set_speed(0.01))

game_app.configure(menu=main_menu)

##########################################
#        Game elements definitions       #
##########################################

class Brick:
    """
    Brick definition.
    """
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.x = 100
        self.y = 100
        self.id = canvas.create_rectangle(20, 20, 50, 50, fill=color)
        self.move_brick()

    def move_brick(self):
        pos = self.canvas.coords(self.id)
        self.canvas.move(self.id, pos[0] * (-1), pos[1] * (-1))
        self.x = random.randint(30, config.height - 60)
        self.y = random.randint(30, 200)
        self.canvas.move(self.id, self.x, self.y)


class Ball:
    """
    Ball definition with movements and stuff...
    """
    def __init__(self, canvas, paddle, brick, config, color):
        self.canvas = canvas
        self.paddle = paddle
        self.brick = brick
        self.config = config
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)

        start = [-3, -2, -1, 1, 2, 3]
        random.shuffle(start)

        self.x = start[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.config.add_score(1)
                return True
            return False

    def hit_brick(self):
        x_0, y_0, x_1, y_1 = self.canvas.bbox(self.brick.id)
        elements_overlap = canvas.find_overlapping(x_0, y_0, x_1, y_1)

        for overlap in elements_overlap:
            if self.id == overlap:
                self.config.add_score(10)
                return True

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        # Ball movements logic.
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            self.canvas.create_text(300, 200, text="Game Over", font="Arial, 40", fill="red")
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
        if self.hit_paddle(pos):
            delta_x = [0, 1, 2]
            self.y = self.y * (-1)

            # Some movements deviation.
            if self.paddle.x < 0:
                if 0 > self.x > -5:
                    random.shuffle(delta_x)
                    self.x = self.x - delta_x[0]
            else:
                if 0 < self.x < 5:
                    random.shuffle(delta_x)
                    self.x = self.x + delta_x[0]
        if self.hit_brick():
            self.brick.move_brick()


class Paddle:
    """
    Paddle definition with movements and stuff.
    """
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 500)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()

        # Standard speed.
        self.canvas.bind_all('<KeyPress-Left>', lambda event, step=-3: self.turn_left(event, step))
        self.canvas.bind_all('<KeyPress-Right>', lambda event, step=3: self.turn_right(event, step))
        # A little faster.
        self.canvas.bind_all('a', lambda event, step=-5: self.turn_left(event, step))
        self.canvas.bind_all('d', lambda event, step=5: self.turn_right(event, step))

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        # Paddle movements logic.
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt, step):
        self.x = step

    def turn_right(self, evt, step):
        self.x = step


##########################################
#                  Game                  #
##########################################

welcome_text = canvas.create_text(300, 200, text="Configure game and hit SPACE to start!", font="Arial, 20", fill="red")
game_app.update()

while not config.start_game:
    game_app.update_idletasks()
    game_app.update()
    time.sleep(0.01)

canvas.delete(welcome_text)

paddle = Paddle(canvas, 'gray')
brick = Brick(canvas, "gray")
ball = Ball(canvas, paddle, brick, config, 'gray')

canvas.create_text(50, 580, text="SCORE: 0", font="Arial, 15", fill="gray", tag="score")

while 1:
    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
        score = canvas.find_withtag("score")
        current_score = "SCORE: {}".format(config.score)
        canvas.delete(score)
        canvas.create_text(50, 580, text=current_score, font="Arial, 15", fill="gray", tag="score")

    game_app.update_idletasks()
    game_app.update()
    time.sleep(config.game_speed)
