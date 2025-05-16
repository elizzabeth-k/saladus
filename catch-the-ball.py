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
paddle_height = 10 # Not used for creation, but useful for boundary checks
paddle_start_x = (canvas_width - paddle_width) / 2
paddle = canvas.create_rectangle(
    paddle_start_x,
    canvas_height - 30,
    paddle_start_x + paddle_width,
    canvas_height - 20, # y1, y2 for paddle
    fill="blue"
)
paddle_speed = 7 # Pixels per update cycle

# Paddle movement state
moving_left = False
moving_right = False

# Ball
ball_radius = 10 # Made it a bit smaller
ball_diameter = ball_radius * 2
ball = canvas.create_oval(0, 0, ball_diameter, ball_diameter, fill="red")
ball_speed_y = 4 # Renamed for clarity
ball_x = random.randint(0, canvas_width - ball_diameter)
canvas.move(ball, ball_x, 0)

# Score
score = 0
score_text = canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 14), fill="black")

game_over_flag = False # Flag to stop updates after game over

# --- Paddle Movement Functions ---
def start_move_left(event):
    global moving_left
    moving_left = True

def stop_move_left(event):
    global moving_left
    moving_left = False

def start_move_right(event):
    global moving_right
    moving_right = True

def stop_move_right(event):
    global moving_right
    moving_right = False

# Bind KeyPress and KeyRelease events
window.bind("<KeyPress-Left>", start_move_left)
window.bind("<KeyRelease-Left>", stop_move_left)
window.bind("<KeyPress-Right>", start_move_right)
window.bind("<KeyRelease-Right>", stop_move_right)

# --- Game Logic ---
def update():
    global score, game_over_flag

    if game_over_flag:
        return # Stop updating if game is over

    # --- Paddle Movement ---
    paddle_pos = canvas.coords(paddle)
    if moving_left and paddle_pos[0] > 0:
        canvas.move(paddle, -paddle_speed, 0)
        # Ensure paddle doesn't go beyond left edge
        if canvas.coords(paddle)[0] < 0:
            canvas.coords(paddle, 0, paddle_pos[1], paddle_width, paddle_pos[3])
    if moving_right and paddle_pos[2] < canvas_width:
        canvas.move(paddle, paddle_speed, 0)
        # Ensure paddle doesn't go beyond right edge
        if canvas.coords(paddle)[2] > canvas_width:
            canvas.coords(paddle, canvas_width - paddle_width, paddle_pos[1], canvas_width, paddle_pos[3])


    # --- Ball Movement ---
    canvas.move(ball, 0, ball_speed_y)
    ball_pos = canvas.coords(ball) # [x1, y1, x2, y2]

    # --- Collision Detection ---
    # Paddle collision
    # Check if ball's bottom edge (ball_pos[3]) is at or below paddle's top edge (paddle_pos[1])
    # AND ball's top edge (ball_pos[1]) is above paddle's bottom edge (paddle_pos[3]) (prevents catching from below)
    # AND ball horizontally overlaps with the paddle
    if (ball_pos[3] >= paddle_pos[1] and ball_pos[1] < paddle_pos[3] and
        ((paddle_pos[0] < ball_pos[0] < paddle_pos[2]) or  # Ball's left edge in paddle
         (paddle_pos[0] < ball_pos[2] < paddle_pos[2]))):  # Ball's right edge in paddle
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")
        reset_ball()
    # Ball missed (hits bottom)
    elif ball_pos[3] > canvas_height:
        canvas.create_text(canvas_width//2, canvas_height//2, text="Game Over!", font=("Arial", 24), fill="darkred", tags="gameover_text")
        game_over_flag = True # Set flag to stop game
        return # Exit update early

    # Game loop: ~33 FPS
    window.after(30, update)

# Reset ball to the top
def reset_ball():
    new_ball_x = random.randint(0, canvas_width - ball_diameter)
    # Current coords of ball: cx1, cy1, cx2, cy2
    # Desired coords: new_ball_x, 0, new_ball_x + ball_diameter, ball_diameter
    # canvas.coords can directly set new coordinates
    canvas.coords(ball, new_ball_x, 0, new_ball_x + ball_diameter, ball_diameter)


# Focus on the window to receive key events immediately
window.focus_set()

# Start the game
update()
window.mainloop()
