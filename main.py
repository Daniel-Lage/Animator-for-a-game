from dataclasses import dataclass
import json
from tkinter import filedialog
from typing import Any, List
import pygame as pg
import os
import Colors


@dataclass
class Div:
    text: str = None
    onclick: Any = lambda: None
    shortcut: str = None
    position: List[int] = None
    rect: pg.Rect = None


class Animator:
    # constants
    pg.init()

    font_file = os.listdir("font")[0]
    large_font = pg.font.Font(f"font/{font_file}", 48)
    medium_font = pg.font.Font(f"font/{font_file}", 32)
    small_font = pg.font.Font(f"font/{font_file}", 16)

    image_names = None
    image_files = None
    image_index = 0

    action = 0
    pressing = 0

    top_left = [0, 0]
    size = [0, 0]

    rectangles = []
    selected = []

    corner1 = [0, 0]
    corner2 = [0, 0]

    looping = True
    ctrl = False

    @classmethod
    def update(cls):
        img = cls.image_files[cls.image_index]
        size = img.get_size()
        cls.width = size[0] if size[0] >= cls.minwidth else cls.minwidth
        cls.height = size[1] + 39
        pg.display.set_mode((cls.width, cls.height))

    @classmethod
    def stop(cls):
        cls.looping = False

    @classmethod
    def load(cls):
        cls.image_names = list(
            filedialog.askopenfilenames(
                filetypes=[
                    ("Images", ".jpeg"),
                    ("Images", ".png"),
                    ("Images", ".jpg"),
                ],
                initialdir="C:/Users/Daniel Lage/Pictures",
            )
        )
        cls.image_files = list(
            pg.image.load(x).convert_alpha() for x in cls.image_names
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

    @classmethod
    def prev_action(cls):
        cls.action -= 1 if cls.action > 0 else -2

    @classmethod
    def next_action(cls):
        cls.action += 1 if cls.action < 3 - 1 else -2

    @classmethod
    def save_as(cls):
        if cls.image_names:
            image_dir = cls.image_names[cls.image_index]
            image_filename = os.path.basename(image_dir)
            image_name = image_filename.split(".")[0]
            cls.image_names.pop(cls.image_index)
            cls.image_files.pop(cls.image_index)
            cls.image_index -= 1 if cls.image_index == len(cls.image_names) else 0
            with open(f"frames/{image_name}.json", "w") as f:
                cls.rectangles.extend(cls.selected)
                cls.selected.clear()

                frame = [
                    [
                        [
                            rect.x,
                            rect.y,
                            rect.width,
                            rect.height,
                        ]
                        for rect in cls.rectangles
                    ],
                ]
                f.write(json.dumps(frame))
                cls.rectangles.clear()

    actions = {
        0: "Drawing",
        1: "Selecting",
        2: "Dragging",
    }

    buttons = (
        Div("Load File(s)", lambda: Animator.load(), "L"),
        Div("Previous", lambda: Animator.prev(), "P"),
        Div("Next", lambda: Animator.next(), "A"),
        Div("Previous Action", lambda: Animator.prev_action(), "PA"),
        Div("A", lambda: None, "A"),
        Div("Next Action", lambda: Animator.next_action(), "NA"),
        Div("Save", lambda: Animator.save_as(), "S"),
    )
    hovered = None

    position = 5
    for button in buttons:
        if button.text == "A":
            size = small_font.size("0")
        else:
            size = small_font.size(button.text)
        size = list(size)
        button.position = position
        button.rect = pg.Rect(button.position, 5, size[0] + 10, size[1] + 10)
        position += 20 + size[0]
    minwidth = position
    width, height = minwidth, 39
    screen = pg.display.set_mode((width, height))

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

                if pg.key.get_pressed()[pg.K_LCTRL]:
                    if event.key == pg.K_q:
                        cls.prev()
                    elif event.key == pg.K_w:
                        cls.next()
                    elif event.key == pg.K_a:
                        cls.load()
                    elif event.key == pg.K_s:
                        cls.save_as()
                else:
                    if event.key == pg.K_q:
                        cls.prev_action()
                    elif event.key == pg.K_w:
                        cls.next_action()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if cls.hovered:  # if a button is hovered do its onclick function
                    cls.hovered.onclick()
                elif mpos[1] > 38:
                    cls.pressing = 1
                    cls.corner1 = mpos

            elif event.type == pg.MOUSEBUTTONUP:
                if cls.pressing:
                    if cls.action == 0:
                        cls.rectangles.append(
                            pg.Rect(
                                cls.top_left[0],
                                cls.top_left[1],
                                cls.size[0],
                                cls.size[1],
                            )
                        )

                    elif cls.action == 1:
                        selection = pg.Rect(
                            cls.top_left[0], cls.top_left[1], cls.size[0], cls.size[1]
                        )
                        cls.rectangles.extend(cls.selected)
                        for rect in cls.rectangles:
                            if rect.colliderect(selection):
                                cls.rectangles.remove(rect)
                                cls.selected.append(rect)

                cls.pressing = 0

        if cls.image_files:
            cls.screen.blit(
                cls.image_files[cls.image_index],
                (0, 39),
            )

        for rect in cls.rectangles:
            pg.draw.rect(
                cls.screen,
                Colors.Rectangle,
                rect,
                2,
            )
        for rect in cls.selected:
            pg.draw.rect(
                cls.screen,
                Colors.Selection,
                rect,
                2,
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

            if cls.action == 0:
                pg.draw.rect(
                    cls.screen,
                    Colors.Rectangle,
                    (cls.top_left[0], cls.top_left[1], cls.size[0], cls.size[1]),
                    2,
                )

            elif cls.action == 1:
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

            elif cls.action == 2:
                mrel = mpos[0] - cls.corner1[0], mpos[1] - cls.corner1[1]
                cls.corner1 = mpos
                for rect in cls.selected:
                    rect[0] += mrel[0]
                    rect[1] += mrel[1]

        pg.draw.rect(
            cls.screen,
            Colors.UIBackground,
            (0, 0, cls.width, 39),
        )

        cls.hovered = None
        for button in cls.buttons:
            text = button.text
            if text == "ACTION":
                text = str(cls.action)

            size = cls.small_font.size(text)
            button_rect = pg.Rect(button.position, 5, size[0] + 10, size[1] + 10)
            shortcut = None
            if button_rect.collidepoint(mpos) and not cls.pressing:
                cls.hovered = button
                pg.draw.rect(
                    cls.screen,
                    Colors.UIBackgroundHovered,
                    button_rect,
                    border_radius=5,
                )

            cls.screen.blit(
                cls.small_font.render(text, True, Colors.Text),
                (button.position + 5, 10),
            )

        if cls.hovered:
            if cls.hovered.shortcut:
                shortcut = {
                    "L": "(Ctrl + A)",
                    "P": "(Ctrl + Q)",
                    "N": "(Ctrl + W)",
                    "PA": "(Q) "
                    + cls.actions[cls.action - 1 if cls.action > 0 else cls.action + 2],
                    "A": cls.actions[cls.action],
                    "NA": "(W) "
                    + cls.actions[cls.action + 1 if cls.action < 2 else cls.action - 2],
                    "S": "(Ctrl + S)",
                }[cls.hovered.shortcut]

                if shortcut:
                    shortcut_size = cls.small_font.size(shortcut)
                    shortcut_pos = [mpos[0], mpos[1] - 14]

                    if shortcut_pos[0] + shortcut_size[0] >= cls.width:
                        shortcut_pos[0] -= shortcut_size[0]

                    pg.draw.rect(
                        cls.screen,
                        Colors.UIBackground,
                        (
                            shortcut_pos[0],
                            shortcut_pos[1],
                            shortcut_size[0],
                            shortcut_size[1],
                        ),
                    )
                    pg.draw.rect(
                        cls.screen,
                        Colors.Text,
                        (
                            shortcut_pos[0],
                            shortcut_pos[1],
                            shortcut_size[0],
                            shortcut_size[1],
                        ),
                        1,
                    )
                    cls.screen.blit(
                        cls.small_font.render(shortcut, True, Colors.Text),
                        shortcut_pos,
                    )

        return cls.looping


while Animator.loop():
    pass
