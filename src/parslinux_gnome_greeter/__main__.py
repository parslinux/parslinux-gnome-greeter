#!/usr/bin/env python3
from .appinfo import APP_ID
import sys
import os
import gi

# Gettext setup - must be done before any other imports
from .translation import init_translation
init_translation()

# Enable translation support for UI files
Gtk = None  # Will be imported later

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gio, GLib, Gtk, Adw

def load_gresource():
    """Loads the GResource file from dev build, XDG_DATA_DIRS, or system prefixes."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    build_dir = os.path.join(project_root, 'build')

    candidates = [
        # 1. Local build directory (development)
        os.path.join(build_dir, 'parslinux-gnome-greeter.gresource'),
    ]

    # 2. XDG_DATA_DIRS paths
    xdg_data_dirs = os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share").split(":")
    for data_dir in xdg_data_dirs:
        if data_dir:
            candidates.append(os.path.join(data_dir, 'parslinux', 'parslinux-gnome-greeter', 'parslinux-gnome-greeter.gresource'))

    # 3. Standard fallback locations
    candidates.extend([
        "/usr/share/parslinux/parslinux-gnome-greeter/parslinux-gnome-greeter.gresource",
        "/usr/local/share/parslinux/parslinux-gnome-greeter/parslinux-gnome-greeter.gresource",
        os.path.expanduser("~/.local/share/parslinux/parslinux-gnome-greeter/parslinux-gnome-greeter.gresource")
    ])

    resource_path = None
    for cand in candidates:
        if os.path.exists(cand):
            resource_path = cand
            break

    if not resource_path:
        print(f"FATAL: Could not find parslinux-gnome-greeter.gresource in candidate locations: {candidates[:4]}")
        sys.exit(1)

    try:
        resource = Gio.resource_load(resource_path)
        Gio.Resource._register(resource)
        print(f"GResource loaded from {resource_path}")
    except GLib.Error as e:
        print(f"FATAL: Could not load GResource from {resource_path}: {e}")
        sys.exit(1)

# Load GResource before importing any UI code
load_gresource()

# Import UI classes after GResource is loaded
from .main_window import MainWindow
from .managers.settings import app_settings
from .managers.shortcut_manager import ShortcutManager

class ParsLinuxGreeterApplication(Adw.Application):
    """The main application."""

    def __init__(self):
        super().__init__(application_id=APP_ID,
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.win = None
        self.is_first_run_check = False
        self.start_page = None

        self.add_main_option(
            "first-run",
            ord("c"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Check if this is the first run (for autostart)",
            None,
        )
        self.add_main_option(
            "page",
            ord("p"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.STRING,
            "First page to be opened of application",
            "PAGE",
        )

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()

        if "first-run" in options:
            self.is_first_run_check = True

        if "page" in options:
            self.start_page = options["page"]

        self.activate()
        return 0

    def do_activate(self):
        """Called when the application is activated."""
        # First run check
        if self.is_first_run_check:
            if not app_settings.get('first-run'):
                print("Autostart check: Not the first run, exiting.")
                self.quit()
                return
            
            # Apply shortcuts only on the actual first run
            print("--- First run detected, applying shortcuts ---")
            shortcut_manager = ShortcutManager()
            shortcut_manager.apply_standard_shortcuts()
            shortcut_manager.apply_custom_shortcuts()
        
        # Normal GUI mode
        if not self.win:
            self.win = MainWindow(application=self, start_page=self.start_page)
        self.win.present()

        if self.is_first_run_check:
            app_settings.set('first-run', False)

def main():
    """The main entry point of the application."""
    app = ParsLinuxGreeterApplication()
    return app.run(sys.argv)

if __name__ == '__main__':
    sys.exit(main()) 