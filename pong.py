import turtle
import winsound
import pygame

# Initialize Pygame sound system
pygame.mixer.init()

# Sound file paths
BOUNCE_SOUND = "ball.wav"
SCORE_SOUND = "point.mp3"
WIN_SOUND = "win.wav"

# Sound playing functions
def play_wav_sound(filename):
    winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)

def play_mp3_sound(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

# Paddle class
class Paddle(turtle.Turtle):
    def __init__(self, position, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

    def move_up(self):
        if self.ycor() < 250:
            self.sety(self.ycor() + 20)

    def move_down(self):
        if self.ycor() > -250:
            self.sety(self.ycor() - 20)

# Ball class
class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.goto(0, 0)
        self.dx = 2
        self.dy = 2

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_y(self):
        self.dy *= -1

    def bounce_x(self):
        self.dx *= -1
        self.dx *= 1.2
        self.dy *= 1.2
        MAX_SPEED = 15
        if abs(self.dx) > MAX_SPEED:
            self.dx = MAX_SPEED if self.dx > 0 else -MAX_SPEED
        if abs(self.dy) > MAX_SPEED:
            self.dy = MAX_SPEED if self.dy > 0 else -MAX_SPEED

    def reset_position(self):
        self.goto(0, 0)
        self.dx = 2 if self.dx > 0 else -2
        self.dy = 2 if self.dy > 0 else -2

# Scoreboard class
class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score_left = 0
        self.score_right = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_score()

    def update_score(self):
        self.clear()
        self.goto(0, 260)
        self.write(f"Left: {self.score_left}    Right: {self.score_right}", align="center", font=("Courier", 24, "normal"))

    def left_scores(self):
        self.score_left += 1
        self.update_score()

    def right_scores(self):
        self.score_right += 1
        self.update_score()

    def show_winner(self, winner_text):
        self.goto(0, 0)
        self.write(winner_text, align="center", font=("Courier", 30, "bold"))

# Game class
class Game:
    def __init__(self):
        self.left_paddle_color = "white"
        self.right_paddle_color = "yellow"
        self.background_color = "black"
        self.theme_chosen = False

        self.screen = turtle.Screen()
        self.screen.title("Pong Game - Turtle Version")
        self.screen.setup(width=800, height=600)
        self.screen.bgcolor("black")
        self.screen.tracer(0)

        self.message_writer = turtle.Turtle()
        self.message_writer.hideturtle()
        self.message_writer.penup()
        self.message_writer.color("white")

        self.choose_theme()
        self.screen.update()

        self.left_paddle = Paddle(position=(-350, 0), color=self.left_paddle_color)
        self.right_paddle = Paddle(position=(350, 0), color=self.right_paddle_color)
        self.ball = Ball()
        self.scoreboard = Scoreboard()

        self.game_is_on = True
        self.bind_keys()

        print("Choose Theme: 1 - Classic, 2 - Space, 3 - Nature")
        print("After selecting theme, press SPACE to start the game.")
        self.screen.onkeypress(self.start_game, "space")
        self.screen.onkeypress(self.restart_game, "r")

    def show_message_on_screen(self, message):
        self.message_writer.clear()
        self.message_writer.goto(0, 200)
        self.message_writer.write(message, align="center", font=("Courier", 16, "bold"))

    def choose_theme(self):
        def set_theme(choice):
            if choice == "1":
                self.background_color = "black"
                self.left_paddle_color = "white"
                self.right_paddle_color = "yellow"
            elif choice == "2":
                self.background_color = "midnight blue"
                self.left_paddle_color = "light blue"
                self.right_paddle_color = "pink"
            elif choice == "3":
                self.background_color = "#004953"
                self.left_paddle_color = "#F5F5DC"
                self.right_paddle_color = "orange"
            self.theme_chosen = True
            print("Theme selected. Press SPACE to start the game.")
            self.show_message_on_screen("Press SPACE to start the game.")

        self.screen.listen()
        self.screen.onkeypress(lambda: set_theme("1"), "1")
        self.screen.onkeypress(lambda: set_theme("2"), "2")
        self.screen.onkeypress(lambda: set_theme("3"), "3")
        self.show_message_on_screen("Press 1, 2 or 3 to choose a theme.\nThen press SPACE to start the game.")

    def bind_keys(self):
        self.screen.listen()
        self.screen.onkeypress(self.left_paddle.move_up, "w")
        self.screen.onkeypress(self.left_paddle.move_down, "s")
        self.screen.onkeypress(self.right_paddle.move_up, "Up")
        self.screen.onkeypress(self.right_paddle.move_down, "Down")

    def start_game(self):
        if not self.theme_chosen or not self.game_is_on:
            return
        self.left_paddle.color(self.left_paddle_color)
        self.right_paddle.color(self.right_paddle_color)
        self.message_writer.clear()
        self.screen.bgcolor(self.background_color)
        self.update_game()

    def restart_game(self):
        self.scoreboard.clear()
        self.scoreboard.score_left = 0
        self.scoreboard.score_right = 0
        self.scoreboard.update_score()
        self.message_writer.clear()
        self.ball.reset_position()
        self.left_paddle.goto(-350, 0)
        self.right_paddle.goto(350, 0)
        self.game_is_on = True
        self.update_game()

    def update_game(self):
        if not self.game_is_on:
            return

        self.screen.bgcolor(self.background_color)
        self.screen.update()
        self.ball.move()

        # Ball hits top/bottom
        if self.ball.ycor() > 290 or self.ball.ycor() < -290:
            self.ball.bounce_y()
            play_wav_sound(BOUNCE_SOUND)

        # Ball hits right paddle
        if self.ball.distance(self.right_paddle) < 50 and self.ball.xcor() > 320:
            self.ball.setx(320)
            self.ball.bounce_x()
            play_wav_sound(BOUNCE_SOUND)

        # Ball hits left paddle
        if self.ball.distance(self.left_paddle) < 50 and self.ball.xcor() < -320:
            self.ball.setx(-320)
            self.ball.bounce_x()
            play_wav_sound(BOUNCE_SOUND)

        # Ball missed by right paddle
        if self.ball.xcor() > 390:
            self.ball.reset_position()
            self.scoreboard.left_scores()
            play_mp3_sound(SCORE_SOUND)

        # Ball missed by left paddle
        if self.ball.xcor() < -390:
            self.ball.reset_position()
            self.scoreboard.right_scores()
            play_mp3_sound(SCORE_SOUND)

        # Win condition
        if self.scoreboard.score_left >= 5:
            self.scoreboard.clear()
            self.scoreboard.goto(0, 50)
            self.scoreboard.write("Left Player Wins!", align="center", font=("Courier", 30, "bold"))
            self.message_writer.goto(0, -50)
            self.message_writer.write("Game Over\nPress R to Restart", align="center", font=("Courier", 20, "bold"))
            play_wav_sound(WIN_SOUND)
            self.game_is_on = False
            return
        elif self.scoreboard.score_right >= 5:
            self.scoreboard.clear()
            self.scoreboard.goto(0, 50)
            self.scoreboard.write("Right Player Wins!", align="center", font=("Courier", 30, "bold"))
            self.message_writer.goto(0, -50)
            self.message_writer.write("Game Over\nPress R to Restart", align="center", font=("Courier", 20, "bold"))
            play_wav_sound(WIN_SOUND)
            self.game_is_on = False
            return

        self.screen.ontimer(self.update_game, 20)

    def play(self):
        self.screen.mainloop()

# Start the game
game = Game()
game.play()





