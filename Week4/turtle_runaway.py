# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random, time, os

WIDTH = 700
HEIGHT = 700

# stage enum
# 0: chasing
# 1: catched
# 2: escaped
# 3: lose
# 4: win

class RunawayGame:
    def __init__(self, stage, canvas, player, robot, dest, catch_radius=20):
        self.stage = stage
        self.next_stage_time = 0
        self.canvas = canvas
        self.player = player
        self.robot = robot
        self.dest = dest
        self.catch_radius2 = catch_radius**2

        self.start_time = time.time()

        # Initialize 'runner' and 'chaser'
        self.player.shape(os.path.join(os.path.dirname(__file__), 'rabbit.gif'))
        self.player.color('blue')
        self.player.hideturtle()
        self.player.penup()

        self.robot.shape('turtle')
        self.robot.color('green')
        self.robot.hideturtle()
        self.robot.penup()

        self.dest.shape(os.path.join(os.path.dirname(__file__), 'king.gif'))
        self.dest.hideturtle()
        self.dest.penup()

        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        self.drawer.setpos(-330, 300)
        self.drawer.write('별/주/부/전 리벤져', font=('Courier', 30, 'bold'))
        self.drawer.setpos(-330, 270)
        self.drawer.write('Catch the tortoise for its liver', font=('Courier', 20))
        
        self.timer = turtle.RawTurtle(canvas)
        self.timer.hideturtle()
        self.timer.penup()
        self.timer.setpos(280, -320)
        self.timer.write(0.00, font=('Courier', 20))

    def is_catched(self, a, b):
        p = a.pos()
        q = b.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, ai_timer_msec=100):
        def randomPosition(distance, object):
            x, y = 0, 0
            while (x - object.pos()[0])**2 + (y - object.pos()[1])**2 < distance**2:
                x, y = random.randint(-WIDTH, WIDTH - 20), random.randint(-HEIGHT, HEIGHT - 20)
            return x/2, y/2

        self.player.setpos(-WIDTH/2 + 10, -HEIGHT/2 + 10)
        self.player.setheading(0)

        self.robot.setpos(randomPosition(WIDTH * 0.2, self.player))
        self.robot.setheading(random.randint(0, 360))

        self.dest.setpos(randomPosition(WIDTH * 0.7, self.player))
        self.dest.setheading(0)

        self.player.showturtle()
        self.robot.showturtle()
        self.dest.showturtle()

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.robot.run_ai()

        # Catch the Tortoise
        if self.is_catched(self.player, self.robot):
            if self.stage[0] == 0:
                self.next_stage_time = time.time() + 2
                self.stage[0] = 1

                self.drawer.undo()
                self.drawer.write('Go to king to escape the angry tortoise', font=('Courier', 20))
            elif self.stage[0] == 2:
                self.stage[0] = 3
                self.drawer.undo()
                self.drawer.write('The angry tortoise catched you. You Lose!', font=('Courier', 20))
        
        # Tortoise is angry
        if self.stage[0] == 1 and time.time() > self.next_stage_time:
            self.stage[0] = 2

        # Go to the King
        if self.is_catched(self.player, self.dest):
            if self.stage[0] == 1 or self.stage[0] == 2:
                self.stage[0] = 4
                self.drawer.undo()
                self.drawer.write('Thanks to you, the Dragon King is healthy. You Win!', font=('Courier', 20))
                self.player.hideturtle()
                self.robot.hideturtle()
                self.dest.hideturtle()

                during = time.time() - self.start_time
                if during < 10:
                    grade = 'S'
                elif during < 20:
                    grade = 'A'
                elif during < 30:
                    grade = 'B'
                elif during < 40:
                    grade = 'C'
                elif during < 50:
                    grade = 'D'
                else:
                    grade = 'E'

                self.drawer.setpos(-60, 90)
                self.drawer.write('Your Score:', font=('Courier', 20))
                self.drawer.setpos(-35, -50)
                self.drawer.write(grade, font=('Courier', 140, 'bold'))
                self.drawer.setpos(-240, -80)
                self.drawer.write('<10s: S  <20s: A  <30s: B  <40s: C  <50s: D  >=50s: E', font=('Courier', 15))

        # Update Timer
        if self.stage[0] < 3:
            self.timer.undo()
            self.timer.write(round(time.time() - self.start_time, 2), font=('Courier', 20))

        self.canvas.ontimer(self.step, self.ai_timer_msec)
        

def inbound(self, do, rollback):
    do(self.step_move)
    x, y = self.pos()
    if not (-WIDTH/2 < x < WIDTH/2) or not (-HEIGHT/2 < y < HEIGHT/2):
        rollback(self.step_move)

class PlayerMover(turtle.RawTurtle):
    def __init__(self, canvas, stage, step_move=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.stage = stage

        def move(self, angle):
            self.setheading(angle)
            inbound(self, self.forward, self.backward)

        # Register event handlers
        canvas.onkeypress(lambda: move(self, 90), 'Up')
        canvas.onkeypress(lambda: move(self, 270), 'Down')
        canvas.onkeypress(lambda: move(self, 180), 'Left')
        canvas.onkeypress(lambda: move(self, 0), 'Right')
        canvas.listen()

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, stage, step_move=20, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.stage = stage

    def run_ai(self):
        if self.stage[0] == 0:
            mode = random.randint(0, 2)
            if mode == 0:
                inbound(self, self.forward, self.backward)
            elif mode == 1:
                self.left(self.step_turn)
            elif mode == 2:
                self.right(self.step_turn)
        elif self.stage[0] == 1:
            self.color('yellow')
        elif self.stage[0] == 2:
            self.color('red')
            pos = player.pos()
            self.setheading(self.towards(pos))
            self.forward(self.step_move * 0.8)

class DestMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    root.title('Turtle Runaway')
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.addshape(os.path.join(os.path.dirname(__file__), 'king.gif'))
    screen.addshape(os.path.join(os.path.dirname(__file__), 'rabbit.gif'))

    stage = [0]

    player = PlayerMover(screen, stage)
    robot = RandomMover(screen, stage)
    dest = DestMover(screen)

    game = RunawayGame(stage, screen, player, robot, dest)
    game.start()
    screen.mainloop()
