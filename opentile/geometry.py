#!/usr/bin/python

from enum import Enum

import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck


GRAVITY = Wnck.WindowGravity.STATIC
RESIZE_MASK = Wnck.WindowMoveResizeMask(255)


def resize_window(window, x, y, width, height):
    window.set_geometry(GRAVITY, RESIZE_MASK, x, y, width, height)


def stack_layout(tw, windows_list):
    if not len(windows_list):
        return
    master = windows_list[0]
    stack = windows_list[1:]

    # Resize Master Window
    if len(stack):
        width = tw.width // 2 - tw.inner_gap // 2 - tw.outer_gap - tw.padding_right
    else:
        width = tw.width - tw.outer_gap * 2 - tw.padding_right
    resize_window(
        master,
        tw.outer_gap + tw.padding_left,
        tw.outer_gap + tw.padding_top,
        width,
        tw.height - tw.outer_gap * 2 - tw.padding_bottom,
    )

    # Resize Stack Windows
    for i, window in enumerate(stack):
        stack_len = len(stack)
        y_cons = tw.height - tw.outer_gap * 2 - tw.inner_gap * (stack_len - 1)
        resize_window(
            window,
            tw.width // 2 + tw.inner_gap // 2,
            tw.outer_gap + (y_cons // stack_len) * i + tw.inner_gap * i,
            tw.width // 2 - tw.inner_gap // 2 - tw.outer_gap,
            (y_cons // stack_len),
        )


class Layout(Enum):
    stack = stack_layout
