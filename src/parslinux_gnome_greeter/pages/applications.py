import gi
import subprocess

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/org/parslinux/parslinux-gnome-greeter/ui/ApplicationsPage.ui')
class ApplicationsPage(Adw.PreferencesPage):
    __gtype_name__ = 'ApplicationsPage'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ApplicationsPage created.")
    
    @Gtk.Template.Callback()
    def on_open_store_clicked(self, button):
        """Open ParsLinux Software Center"""
        try:
            subprocess.Popen(["parslinux-software"])
        except FileNotFoundError:
            print("ParsLinux Software Center not found")
        except Exception as e:
            print(f"Error opening ParsLinux Software Center: {e}") 