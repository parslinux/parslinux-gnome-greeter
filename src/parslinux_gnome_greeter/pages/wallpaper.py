from concurrent.futures import ThreadPoolExecutor
from gettext import gettext as _
import os
import subprocess
import threading

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gdk, GLib, Gtk

from ..appinfo import resource_path as _rp
from ..managers.wallpaper_manager import WallpaperManager

# WallpaperThumbnail template class
@Gtk.Template(resource_path=_rp('ui', 'components', 'WallpaperThumbnail.ui'))
class WallpaperThumbnail(Gtk.Box):
    __gtype_name__ = 'WallpaperThumbnail'
    
    # Template children
    picture = Gtk.Template.Child("picture")
    selected_check = Gtk.Template.Child("selected_check")
    
    def __init__(self):
        super().__init__()
        
        # Set size request
        self.picture.set_size_request(160, 120)
        
        # Selection state
        self._selected = False
        
        # Initially hide checkmark
        self.selected_check.set_opacity(0)
    
    def load_wallpaper(self, wallpaper_path):
        """Load wallpaper from file path"""
        try:
            if os.path.exists(wallpaper_path):
                texture = Gdk.Texture.new_from_filename(wallpaper_path)
                self.picture.set_paintable(texture)
        except Exception as e:
            print(f"Error loading wallpaper {wallpaper_path}: {e}")
    
    def load_pixbuf(self, pixbuf):
        """Load wallpaper from GdkPixbuf"""
        try:
            if pixbuf:
                texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                self.picture.set_paintable(texture)
        except Exception as e:
            print(f"Error loading pixbuf: {e}")
    
    def set_selected(self, selected):
        """Set selection state"""
        self._selected = selected
        
        # Show/hide checkmark
        if selected:
            self.selected_check.set_opacity(1)
        else:
            self.selected_check.set_opacity(0)
    
    def is_selected(self):
        """Get selection state"""
        return self._selected

@Gtk.Template(resource_path=_rp('ui', 'WallpaperPage.ui'))
class WallpaperPage(Adw.PreferencesPage):
    __gtype_name__ = 'WallpaperPage'
    
    # Template children
    live_wallpaper_row = Gtk.Template.Child("live_wallpaper_row")
    wallpapers_flowbox = Gtk.Template.Child("wallpapers_flowbox")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize manager
        self.wallpaper_manager = WallpaperManager()
        self.wallpapers = []
        self.current_selection = None
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="WallpaperThumb")
        self._is_destroyed = False
        
        # Connect signals
        if self.live_wallpaper_row:
            self.live_wallpaper_row.connect("activated", self.on_live_wallpaper_clicked)
        if self.wallpapers_flowbox:
            self.wallpapers_flowbox.connect("child-activated", self.on_wallpaper_selected)
        
        # Load wallpapers in background thread
        thread = threading.Thread(target=self.load_wallpapers_background)
        thread.daemon = True
        thread.start()

    def __del__(self):
        self._is_destroyed = True
        try:
            self._executor.shutdown(wait=False, cancel_futures=True)
        except Exception:
            pass
    
    def load_wallpapers_background(self):
        """Load wallpapers in background thread"""
        try:
            self.wallpapers = self.wallpaper_manager.get_wallpapers()
            GLib.idle_add(self.populate_wallpapers_ui)
        except Exception as e:
            print(f"Error loading wallpapers: {e}")
            
    def populate_wallpapers_ui(self):
        """Populate the UI with wallpaper thumbnails in deterministic order, then load images asynchronously."""
        try:
            if not self.wallpapers or not self.wallpapers_flowbox or self._is_destroyed:
                return
            
            # Get current wallpaper for selection
            current_wallpaper = self.wallpaper_manager.get_current_wallpaper()
            
            # 1. Add all thumbnail widgets in original deterministic order
            tasks = []
            for wallpaper_path in self.wallpapers:
                thumbnail = WallpaperThumbnail()
                child = Gtk.FlowBoxChild()
                child.set_child(thumbnail)
                child.wallpaper_path = wallpaper_path
                child.thumbnail = thumbnail
                
                # Set initial selection state immediately
                if current_wallpaper and wallpaper_path == current_wallpaper:
                    child.add_css_class('active-item')
                    thumbnail.set_selected(True)
                    self.current_selection = child
                
                self.wallpapers_flowbox.append(child)
                tasks.append((wallpaper_path, thumbnail))

            # 2. Submit thumbnail generation tasks to controlled thread pool
            for wallpaper_path, thumbnail in tasks:
                self._executor.submit(self._generate_thumbnail_task, wallpaper_path, thumbnail)
                
        except Exception as e:
            print(f"Error populating wallpapers UI: {e}")

    def _generate_thumbnail_task(self, wallpaper_path, thumbnail):
        """Generate thumbnail in worker thread and dispatch update to main thread."""
        if self._is_destroyed:
            return
        try:
            pixbuf = self.wallpaper_manager.create_thumbnail(wallpaper_path, 160, 120)
            if pixbuf and not self._is_destroyed:
                GLib.idle_add(self._apply_thumbnail, thumbnail, pixbuf)
        except Exception as e:
            print(f"Error creating thumbnail for {wallpaper_path}: {e}")

    def _apply_thumbnail(self, thumbnail, pixbuf):
        """Apply loaded thumbnail pixbuf on the GTK main thread."""
        if not self._is_destroyed and thumbnail:
            thumbnail.load_pixbuf(pixbuf)
        return False

    def on_wallpaper_selected(self, flowbox, flowbox_child):
        """Handle wallpaper selection - GNOME Control Center style"""
        try:
            if not hasattr(flowbox_child, 'wallpaper_path'):
                return
                
            wallpaper_path = flowbox_child.wallpaper_path
            
            # Remove active-item class from previous selection
            if self.current_selection:
                self.current_selection.remove_css_class('active-item')
                if hasattr(self.current_selection, 'thumbnail'):
                    self.current_selection.thumbnail.set_selected(False)
            
            # Add active-item class to new selection
            flowbox_child.add_css_class('active-item')
            if hasattr(flowbox_child, 'thumbnail'):
                flowbox_child.thumbnail.set_selected(True)
            
            self.current_selection = flowbox_child
            
            # Set wallpaper immediately (like GNOME Control Center)
            success = self.wallpaper_manager.set_wallpaper(wallpaper_path)
            if success:
                print(f"Wallpaper changed to: {wallpaper_path}")
            else:
                print(f"Failed to set wallpaper: {wallpaper_path}")
                
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
    
    def on_live_wallpaper_clicked(self, row):
        """Handle ParsLinux Live Wallpaper button click without shell injection or blocking."""
        try:
            extension_uuid = "parslinux-wallpaper-extension@parslinux.org.tr"
            is_installed = False
            try:
                result = subprocess.run(
                    ["gnome-extensions", "prefs", extension_uuid],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                is_installed = (result.returncode == 0)
            except FileNotFoundError:
                is_installed = False

            if not is_installed:
                # Extension not found, show info dialog
                dialog = Adw.MessageDialog.new(
                    self.get_root(),
                    _("Extension Not Found"),
                    _("ParsLinux Live Wallpaper extension is not installed. Please install it from GNOME Extensions.")
                )
                dialog.add_response("ok", _("OK"))
                dialog.set_default_response("ok")
                dialog.set_close_response("ok")
                dialog.present()
                
        except Exception as e:
            print(f"Error opening live wallpaper settings: {e}")
