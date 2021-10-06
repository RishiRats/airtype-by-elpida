from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("1280x720")
window.configure(bg = "#0093FF")


canvas = Canvas(
    window,
    bg = "#0093FF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    720.0,
    fill="#0093FF",
    outline="")

canvas.create_rectangle(
    640.0,
    0.0,
    1280.0,
    720.0,
    fill="#FFFFFF",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    959.0,
    166.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=886.0,
    y=411.0,
    width=179.0,
    height=56.0
)

canvas.create_text(
    118.0,
    316.0,
    anchor="nw",
    text="Developed by Elpida",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 18 * -1)
)

canvas.create_text(
    118.0,
    359.0,
    anchor="nw",
    text="https://github.com/RishiRats ",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 18 * -1)
)

canvas.create_text(
    118.0,
    467.0,
    anchor="nw",
    text="https://github.com/Abhishek-lohar",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 18 * -1)
)

canvas.create_text(
    118.0,
    411.0,
    anchor="nw",
    text="https://github.com/Shridhargpatil",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 18 * -1)
)

canvas.create_text(
    980.0,
    680.0,
    anchor="nw",
    text="Mail us:- dev.elpida@gmail.com",
    fill="#000000",
    font=("Comfortaa Regular", 18 * -1)
)
window.resizable(False, False)
window.title('AIRTYPE By Elpida')
window.mainloop()
