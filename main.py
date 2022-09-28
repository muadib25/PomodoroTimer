from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 20
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
repetitions = 0
timer = str(0)
timer_running = False
timer_paused = True


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global repetitions, timer_running, timer_paused
    timer_running = False
    timer_paused = False
    window.after_cancel(timer)
    repetitions = 0

    # reset text in timer to 00:00
    canvas.itemconfig(timer_text, text="00:00")

    # change title to "Timer"
    title_label.config(text="Timer", fg=GREEN)

    # reset checkmarks
    check_marks.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global timer_running, repetitions, title_label

    if not timer_running:
        timer_running = True
        global repetitions, title_label
        start_timer()

    elif timer_running:
        repetitions += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if repetitions % 8 == 0:
            count_down(long_break_sec)
            title_label.config(text="Break", fg=RED)

            # make a sound when timer ends
            window.bell()

            # Pop window to front when timer changes
            window.attributes("-topmost", True)
            window.lift()
            window.attributes("-topmost", False)

        elif repetitions % 2 == 0:
            count_down(short_break_sec)
            title_label.config(text="Break", fg=PINK)

            # make a sound when timer ends
            window.bell()

            # Pop window to front when timer changes
            window.attributes("-topmost", True)
            window.lift()
            window.attributes("-topmost", False)

        else:
            count_down(work_sec)
            title_label.config(text="Work", fg=GREEN)

            # make a sound when timer ends
            window.bell()

            # Pop window to front when timer changes
            window.attributes("-topmost", True)
            window.lift()
            window.attributes("-topmost", False)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60

    # if count_sec == 0:
    #     count_sec = "00"
    if count_sec < 10:
        # adds a "0" as prefix for the seconds
        count_sec = "%02d" % count_sec
        # or
        # count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(repetitions / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=209, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 27, "bold"))
canvas.grid(column=1, row=1)

# The Timer text
title_label = Label(text="Timer", font=(FONT_NAME, 37, "bold"), fg=GREEN, bg=YELLOW)
title_label.grid(column=1, row=0)


# The Start button
start = Button(text="Start", highlightthickness=0, command=start_timer)
start.grid(column=0, row=2)

# The Reset button
reset = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset.grid(column=2, row=2)

# The Check text
check_marks = Label(font=(FONT_NAME, 20, "bold"), fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()
