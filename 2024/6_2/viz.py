import time
import os

# Frames of ASCII art to simulate animation
frames = [
    r"""
   (\_/)
   (o.o)
   (> <)
   """,
    r"""
    /)/)
   (o.-)
   (> >)
   """,
    r"""
    /)(\
   (o.o)
   (< <)
   """,
]


def clear_screen():
    # Move cursor to top-left and clear screen
    print("\033[H\033[2J", end="")


def animate_ascii(frames, delay=0.5):
    clear_screen()
    # Loop over the frames infinitely
    while True:
        for frame in frames:
            clear_screen()
            print(frame, end="", flush=True)  # Print frame
            time.sleep(delay)


# Run the animation
try:
    animate_ascii(frames)
except KeyboardInterrupt:
    print("\nAnimation stopped.")
