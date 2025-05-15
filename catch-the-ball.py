import tkinter as tk
import random

# Set up window
window = tk.Tk()
window.title("Catch the Ball Game")

# Canvas
canvas_width = 400
canvas_height = 500
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="lightblue")
canvas.pack()

# Paddle (the catcher)
paddle_width = 80
paddle = canvas.create_rectangle(160, 470, 240, 480, fill="blue")

# Ball
ball_radius = 20
ball = canvas.create_oval(0, 0, ball_radius*2, ball_radius*2, fill="red")
ball_speed = 5
ball_x = random.randint(0, canvas_width - ball_radius*2)
canvas.move(ball, ball_x, 0)

# Score
score = 0
score_text = canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 14), fill="black")

# Move paddle with arrow keys
def move_left(event):
    canvas.move(paddle, -20, 0)

def move_right(event):
    canvas.move(paddle, 20, 0)

window.bind("<Left>", move_left)
window.bind("<Right>", move_right)

# Update game
def update():
    global score
    canvas.move(ball, 0, ball_speed)
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    # If ball hits the paddle
    if (paddle_pos[0] < ball_pos[0] < paddle_pos[2] or
        paddle_pos[0] < ball_pos[2] < paddle_pos[2]) and ball_pos[3] >= paddle_pos[1]:
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")
        reset_ball()

    # If ball missed
    elif ball_pos[3] > canvas_height:
        canvas.create_text(canvas_width//2, canvas_height//2, text="Game Over!", font=("Arial", 24), fill="darkred")
        return

    window.after(50, update)

# Reset ball to the top
def reset_ball():
    canvas.coords(ball, 0, 0, ball_radius*2, ball_radius*2)
    canvas.move(ball, random.randint(0, canvas_width - ball_radius*2), 0)

# Start the game
update()
window.mainloop()
