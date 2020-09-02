#!/usr/bin/python

import logging

logging.basicConfig(format="%(levelname)s :: %(message)s", level=logging.DEBUG)

import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck, GLib

import geometry


class TiledWorkspace:
    def __init__(self, tiler, workspace):
        self.tiler = tiler
        self.width = workspace.get_width()
        self.height = workspace.get_height()
        self.number = workspace.get_number()
        self.layout = geometry.Layout.stack
        self.windows = []

        self.outer_gap = 32
        self.inner_gap = 16
        self.padding_top = 0
        self.padding_right = 0
        self.padding_bottom = 0
        self.padding_left = 0

    def add_window(self, window):
        self.windows.append(window)
        if tiler.initialized:
            self.tile()

    def remove_window(self, window):
        self.windows.remove(window)
        if tiler.initialized:
            self.tile()

    def tile(self):
        logging.debug("Tiling workspace %s", self.number)
        self.layout(self, self.windows)


class Tiler:
    def __init__(self):
        self.screen = Wnck.Screen.get_default()
        self.workspaces = {}
        self.initialized = False

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
        window.connect("workspace-changed", self.on_workspace_changed)
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

    def on_workspace_changed(self, window):
        new_workspace = window.get_workspace().get_number()
        logging.debug(
            "Workspace Changed id(%s) workspace(%s)", window.get_pid(), new_workspace
        )
        for workspace in self.workspaces.values():
            if window in workspace.windows:
                workspace.remove_window(window)
        self.workspaces[new_workspace].add_window(window)


if __name__ == "__main__":
    tiler = Tiler()
    tiler.start()
