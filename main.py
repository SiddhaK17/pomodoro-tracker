from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
timer_running = False

# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global reps, timer, timer_running

    if timer is not None:
        window.after_cancel(timer)         #This way we can cancel the timer we had set up previously

    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")

    reps = 0
    timer = None
    timer_running = False

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, timer_running

    if timer_running:
        return

    timer_running = True
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        title_label.config(text="Break", fg=RED)
        count_down(long_break_sec)

    elif reps % 2 == 0:
        title_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)

    else:
        title_label.config(text="Work", fg=GREEN)
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = count // 60
    count_sec = count % 60
    # if count_sec < 10:          #Here we are using dynamic typing to change the data type of count_sec from an integer to a string. And then we use that string to display inside this canvas text
    #     count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min:02d}:{count_sec:02d}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        global timer_running
        timer_running = False

        marks = ""
        work_sessions = reps // 2

        for _ in range(work_sessions):
            marks += "✔"

        check_marks.config(text=marks)

        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
try:
    window.iconphoto(False, PhotoImage(file="tomato.png"))
except Exception:
    pass


title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

#We're going to create our canvas in between our window creation and the window main loop
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)           #"highlightthickness" was the border around our canvas which we made it 0 because it was having white color
tomato_img = PhotoImage(file="tomato.png")              #This is basically a way to read through a file and to get hold of a particular image at a particular file location
canvas.create_image(100, 112, image=tomato_img)      #Here the X value is 100 and Y value is 224 and as we need to position the image in the center, we have taken it half of our Canvas width and height.
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()