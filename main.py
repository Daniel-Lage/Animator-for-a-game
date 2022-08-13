from collections import namedtuple
from dataclasses import dataclass
from tkinter import filedialog
from pyclbr import Function
from turtle import screensize, width
import pygame as pg
import os
import Colors


class Animator:
    Button = namedtuple("Button", ["text", "func"])
    # constants
    width, height = 270, 38

    pg.init()
    screen = pg.display.set_mode((width, height))

    font_file = os.listdir("font")[0]
    large_font = pg.font.Font(f"font/{font_file}", 48)
    medium_font = pg.font.Font(f"font/{font_file}", 32)
    small_font = pg.font.Font(f"font/{font_file}", 16)

    image_files = None
    image_index = 0

    action = 1
    pressing = 0

    top_left = [0, 0]
    size = [0, 0]

    corner1 = [0, 0]
    corner2 = [0, 0]

    looping = True

    @classmethod
    def update(cls):
        img = cls.image_files[cls.image_index]
        size = img.get_size()
        cls.width = size[0] if size[0] >= 270 else 270
        cls.height = size[1] + 39
        pg.display.set_mode((cls.width, cls.height))

    @classmethod
    def stop(cls):
        cls.looping = False

    @classmethod
    def open(cls):
        cls.image_files = tuple(
            pg.image.load(x).convert_alpha()
            for x in filedialog.askopenfilenames(
                filetypes=[
                    ("Images", ".jpeg"),
                    ("Images", ".png"),
                    ("Images", ".jpg"),
                ],
                initialdir="C:/Users/Daniel Lage/Pictures",
            )
        )
        cls.update()

    @classmethod
    def prev(cls):
        cls.image_index -= 1 if cls.image_index > 0 else 0
        cls.update()

    @classmethod
    def next(cls):
        cls.image_index += 1 if cls.image_index < len(cls.image_files) - 1 else 0
        cls.update()

    buttons = (
        Button("Open File", lambda: Animator.open()),
        Button("Previous", lambda: Animator.prev()),
        Button("Next", lambda: Animator.next()),
    )
    hovered: Button = None

    @classmethod
    def loop(cls):
        mpos = pg.mouse.get_pos()
        pg.display.flip()
        cls.screen.fill(Colors.Background)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                cls.stop()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    cls.stop()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if mpos[1] > 38:
                    cls.pressing = 1
                    cls.corner1 = mpos

                elif cls.hovered:  # if a button is hovered do its function
                    cls.hovered.func()

            elif event.type == pg.MOUSEBUTTONUP:
                cls.pressing = 0

        if cls.image_files:
            cls.screen.blit(
                cls.image_files[cls.image_index],
                (0, 39),
            )

        if cls.pressing:
            cls.corner2 = mpos
            cls.top_left[0] = (
                cls.corner1[0] if cls.corner1[0] < cls.corner2[0] else cls.corner2[0]
            )
            cls.top_left[1] = (
                cls.corner1[1] if cls.corner1[1] < cls.corner2[1] else cls.corner2[1]
            )

            cls.size[0] = abs(cls.corner1[0] - cls.corner2[0])

            if cls.top_left[1] < 39:
                cls.top_left[1] = 39
            else:
                cls.size[1] = abs(cls.corner1[1] - cls.corner2[1])

            if cls.action == 1:
                selection = pg.Surface(cls.size)
                selection.set_alpha(128)
                selection.fill(Colors.Selection)
                cls.screen.blit(selection, cls.top_left)
                pg.draw.rect(
                    cls.screen,
                    Colors.SelectionBorder,
                    (cls.top_left[0], cls.top_left[1], cls.size[0], cls.size[1]),
                    1,
                )

        pg.draw.rect(
            cls.screen,
            Colors.UIBackground,
            (0, 0, cls.width, 39),
        )

        position = 0
        cls.hovered = None
        for button in cls.buttons:
            size = cls.small_font.size(button.text)
            button_rect = pg.Rect(position + 5, 5, size[0] + 10, size[1] + 10)

            if button_rect.collidepoint(mpos) and not cls.pressing:
                cls.hovered = button
                pg.draw.rect(
                    cls.screen,
                    Colors.UIBackgroundHovered,
                    button_rect,
                    border_radius=5,
                )

            cls.screen.blit(
                cls.small_font.render(button.text, True, Colors.Text),
                (position + 10, 10),
            )
            position += 20 + size[0]

        return cls.looping


while Animator.loop():
    pass
