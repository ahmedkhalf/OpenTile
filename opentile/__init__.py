#!/usr/bin/python

import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck, GLib

import logging

logging.basicConfig(format="%(levelname)s :: %(message)s", level=logging.DEBUG)


class TiledWorkspace:
    def __init__(self, tiler, workspace):
        self.width = workspace.get_width()
        self.height = workspace.get_height()
        self.number = workspace.get_number()
        self.windows = set()

    def add_window(self, window):
        self.windows.add(window)
        if tiler.initialized:
            self.tile()

    def remove_window(self, window):
        self.windows.remove(window)
        if tiler.initialized:
            self.tile()

    def tile(self):
        logging.debug("Tiling workspace %s", self.number)


class Tiler:
    GRAVITY = Wnck.WindowGravity(0)
    RESIZE_MASK = Wnck.WindowMoveResizeMask(255)

    def __init__(self):
        self.screen = Wnck.Screen.get_default()
        self.workspaces = {}
        self.initialized = False

        self.outer_gap = 32
        self.inner_gap = 16

    def start(self):
        logging.info("Connecting to Signals")
        self.screen.connect("workspace-created", self.on_workspace_created)
        self.screen.connect("workspace-destroyed", self.on_workspace_destroyed)
        self.screen.connect("window-opened", self.on_window_opened)
        self.screen.connect("window_closed", self.on_window_closed)
        logging.info("Signals Connected Successfully")

        logging.info("Initializing")
        self.screen.force_update()
        self.initialized = True
        for workspace in self.workspaces.values():
            if len(workspace.windows):
                workspace.tile()
        logging.info("Successfully Initialized")

        logging.info("Starting Main Loop")
        self.loop = GLib.MainLoop()
        self.loop.run()

    def on_workspace_created(self, _screen, workspace):
        number = workspace.get_number()
        logging.debug("Workspace Created %s", number)
        self.workspaces[number] = TiledWorkspace(self, workspace)

    def on_workspace_destroyed(self, _screen, workspace):
        number = workspace.get_number()
        logging.debug("Workspace Destroyed %s", number)
        self.workspaces.pop(number)

    def on_window_opened(self, _screen, window):
        number = window.get_workspace().get_number()
        logging.debug(
            "Window Opened type(%s) workspace(%s) id(%s)",
            str(window.get_window_type()).split()[1],
            number,
            window.get_pid(),
        )
        self.workspaces[number].add_window(window)

    def on_window_closed(self, _screen, window):
        number = window.get_workspace().get_number()
        logging.debug(
            "Window Closed type(%s) workspace(%s) id(%s)",
            str(window.get_window_type()).split()[1],
            number,
            window.get_pid(),
        )
        self.workspaces[number].remove_window(window)


if __name__ == "__main__":
    tiler = Tiler()
    tiler.start()
