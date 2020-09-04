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

    x_off = tw.padding_right
    y_off = tw.padding_top
    tw_height = tw.height - tw.padding_top - tw.padding_bottom
    tw_width = tw.width - tw.padding_right - tw.padding_left

    # Resize Master Window
    if len(stack):
        width = tw_width // 2 - tw.inner_gap // 2 - tw.outer_gap
    else:
        width = tw_width - tw.outer_gap * 2
    resize_window(
        master,
        tw.outer_gap + x_off,
        tw.outer_gap + y_off,
        width,
        tw_height - tw.outer_gap * 2,
    )

    # Resize Stack Windows
    for i, window in enumerate(stack):
        stack_len = len(stack)
        y_cons = tw_height - tw.outer_gap * 2 - tw.inner_gap * (stack_len - 1)
        resize_window(
            window,
            tw_width // 2 + tw.inner_gap // 2 + x_off,
            tw.outer_gap + (y_cons // stack_len) * i + tw.inner_gap * i + y_off,
            tw_width // 2 - tw.inner_gap // 2 - tw.outer_gap,
            (y_cons // stack_len),
        )


class Layout(Enum):
    stack = stack_layout
