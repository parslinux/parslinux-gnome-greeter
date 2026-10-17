from ..appinfo import resource_path as _rp
import gi
import subprocess
from locale import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw


@Gtk.Template(resource_path=_rp('ui', 'ApplicationsPage.ui'))
class ApplicationsPage(Adw.PreferencesPage):
    __gtype_name__ = 'ApplicationsPage'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_open_store_clicked(self, button):
        """Open ParsLinux Software Center or fallback store"""
        store_candidates = [
            ["parslinux-software"],
            ["gnome-software"],
            ["pamac-manager"],
            ["discover"],
        ]

        for cmd in store_candidates:
            try:
                subprocess.Popen(cmd)
                return
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Error launching '{cmd[0]}': {e}")

        # If no store was found, inform the user
        print("Warning: No software center found on the system.")
        root = self.get_root()
        if isinstance(root, Gtk.Window):
            heading_text = _("Software Center Not Found")
            body_text = _("Could not find a supported software center (parslinux-software or gnome-software) on this system.")
            ok_text = _("OK")
            if hasattr(Adw, "AlertDialog"):
                dialog = Adw.AlertDialog(heading=heading_text, body=body_text)
                dialog.add_response("ok", ok_text)
                dialog.present(root)
            elif hasattr(Adw, "MessageDialog"):
                dialog = Adw.MessageDialog(transient_for=root, heading=heading_text, body=body_text)
                dialog.add_response("ok", ok_text)
                dialog.present()