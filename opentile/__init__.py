#!/usr/bin/python

import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck, GLib


# def onWindowOpen(aScreen, aWindow):
#     print("Window Opened!!")


class Tiler:
    GRAVITY = Wnck.WindowGravity(0)
    RESIZE_MASK = Wnck.WindowMoveResizeMask(255)

    def __init__(self, screen):
        self.screen = screen
        # self.screen.connect("window-opened", onWindowOpen)
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.outer_gap = 32
        self.inner_gap = 16

    def get_active_window(self):
        return self.screen.get_active_window()

    def get_active_workspace(self):
        return self.screen.get_active_workspace()

    def get_windows(self):
        return self.screen.get_windows()

    def get_workspace_windows(self, workspace):
        windows = []
        for window in self.get_windows():
            if window.get_workspace() == workspace:
                windows.append(window)
        return windows

    def set_window_geometry(self, window, x, y, width, height):
        window.set_geometry(Tiler.GRAVITY, Tiler.RESIZE_MASK, x, y - 30, width, height)

    def tile(self):
        active_workspace = self.get_active_workspace()
        windows = self.get_workspace_windows(active_workspace)

        master = self.get_active_window()
        stack = [window for window in windows if window != master]

        if master is None:
            if len(stack) > 0:
                master = stack[0]
                stack.pop(0)
            else:
                return

        # Resize Master Window
        self.set_window_geometry(
            master,
            self.outer_gap,
            self.outer_gap,
            self.width // 2 - self.inner_gap // 2 - self.outer_gap
            if len(stack) > 0
            else self.width - self.outer_gap * 2,
            self.height - self.outer_gap * 2,
        )

        # Resize Stack
        for i, window in enumerate(stack):
            self.set_window_geometry(
                window,
                self.width // 2 + self.inner_gap // 2,
                self.outer_gap
                + (
                    (
                        self.height
                        - self.outer_gap * 2
                        - self.inner_gap * (len(stack) - 1)
                    )
                    // len(stack)
                )
                * i
                + self.inner_gap * i,
                self.width // 2 - self.inner_gap // 2 - self.outer_gap,
                (
                    (
                        self.height
                        - self.outer_gap * 2
                        - self.inner_gap * (len(stack) - 1)
                    )
                    // len(stack)
                ),
            )


screen = Wnck.Screen.get_default()
screen.force_update()

tiler = Tiler(screen)
tiler.tile()

# loop = GLib.MainLoop()
# loop.run()
