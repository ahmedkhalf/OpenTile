#!/usr/bin/python

import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck, GLib


class TiledWorkspace:
    def __init__(self, workspace):
        self.width = workspace.get_width()
        self.height = workspace.get_height()
        self.windows = set()

    def add_window(self, window):
        self.windows.add(window)

    def remove_window(self, window):
        self.windows.remove(window)


class Tiler:
    GRAVITY = Wnck.WindowGravity(0)
    RESIZE_MASK = Wnck.WindowMoveResizeMask(255)

    def __init__(self):
        self.screen = Wnck.Screen.get_default()
        self.workspaces = {}

        self.outer_gap = 32
        self.inner_gap = 16

    def start(self):
        self.screen.connect("workspace-created", self.on_workspace_created)
        self.screen.connect("workspace-destroyed", self.on_workspace_destroyed)
        self.screen.connect("window-opened", self.on_window_opened)
        self.screen.connect("window_closed", self.on_window_closed)

        self.loop = GLib.MainLoop()
        self.loop.run()

    def on_workspace_created(self, _screen, workspace):
        number = workspace.get_number()
        print("+ Workspace Created", number)
        self.workspaces[number] = TiledWorkspace(workspace)

    def on_workspace_destroyed(self, _screen, workspace):
        number = workspace.get_number()
        print("- Workspace Destroyed", number)
        self.workspaces.pop(number)

    def on_window_opened(self, _screen, window):
        print("-" * 40)
        print("+ Window Opened", window.get_window_type())
        self.workspaces[window.get_workspace().get_number()].add_window(window)
        for workspace in self.workspaces:
            print(self.workspaces[workspace].windows)

    def on_window_closed(self, _screen, window):
        print("-" * 40)
        print("- Window Closed")
        self.workspaces[window.get_workspace().get_number()].remove_window(window)
        for workspace in self.workspaces:
            print(self.workspaces[workspace].windows)


if __name__ == "__main__":
    tiler = Tiler()
    tiler.start()
