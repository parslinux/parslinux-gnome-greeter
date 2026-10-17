from ..appinfo import resource_path as _rp
import json
import os
from gi.repository import Gio, GLib


class ExtensionManager:
    def __init__(self, extensions_file=_rp('json', 'extensions.json')):
        self.extensions_file = extensions_file
        self.extensions = self._load_extensions()
        self._proxy = None
        self._init_proxy()

    def _init_proxy(self):
        """Initializes a standard Gio.DBusProxy connection to GNOME Shell Extensions."""
        try:
            if hasattr(Gio, "DBusProxy") and hasattr(Gio.DBusProxy, "new_for_bus_sync"):
                self._proxy = Gio.DBusProxy.new_for_bus_sync(
                    Gio.BusType.SESSION,
                    Gio.DBusProxyFlags.NONE,
                    None,
                    "org.gnome.Shell.Extensions",
                    "/org/gnome/Shell/Extensions",
                    "org.gnome.Shell.Extensions",
                    None
                )
        except Exception as e:
            print(f"Could not connect to GNOME Shell Extensions D-Bus: {e}")
            self._proxy = None

    def _load_extensions(self):
        """Load extensions from JSON file in GResource with fallback to filesystem"""
        # Try GResource first
        try:
            file = Gio.File.new_for_uri(f'resource://{self.extensions_file}')
            success, data, _ = file.load_contents(None)
            if success:
                json_data = data.decode('utf-8')
                return json.loads(json_data)
        except Exception:
            pass  # Fall through to filesystem fallback

        # Fallback: Try to load from filesystem
        try:
            filename = os.path.basename(self.extensions_file)
            fallback_paths = [
                f"/usr/share/parslinux-gnome-greeter/json/{filename}",
                f"/usr/local/share/parslinux-gnome-greeter/json/{filename}",
            ]

            for fallback_path in fallback_paths:
                if os.path.exists(fallback_path):
                    with open(fallback_path, 'r', encoding='utf-8') as f:
                        return json.load(f)

            print(f"Warning: Could not load extensions from GResource ({self.extensions_file}) or filesystem")
            return []
        except Exception as e:
            print(f"Error loading extensions: {e}")
            return []

    def get_extensions(self):
        """Get all extensions"""
        return self.extensions

    def get_enabled_extensions(self):
        """Get currently enabled extensions"""
        if not self._proxy:
            return self._get_enabled_extensions_fallback()

        enabled_extensions = []
        try:
            extensions = self._proxy.ListExtensions()
            if isinstance(extensions, dict):
                for ext_id, ext_info in extensions.items():
                    if isinstance(ext_info, dict) and ext_info.get('state') == 1:
                        enabled_extensions.append(ext_id)
        except Exception as e:
            print(f"Failed to get enabled extensions via D-Bus: {e}")
            return self._get_enabled_extensions_fallback()
        return enabled_extensions

    def _get_enabled_extensions_fallback(self):
        """Fallback to GSettings when D-Bus is unavailable."""
        try:
            source = Gio.SettingsSchemaSource.get_default() if hasattr(Gio, "SettingsSchemaSource") else None
            if source and source.lookup("org.gnome.shell", True):
                shell_settings = Gio.Settings.new("org.gnome.shell")
                return list(shell_settings.get_strv("enabled-extensions"))
        except Exception:
            pass
        return []

    def is_extension_enabled(self, extension_id):
        """Check if an extension is enabled"""
        if not self._proxy:
            return extension_id in self._get_enabled_extensions_fallback()
        try:
            extensions = self._proxy.ListExtensions()
            if isinstance(extensions, dict) and extension_id in extensions:
                ext_info = extensions[extension_id]
                return isinstance(ext_info, dict) and ext_info.get('state') == 1
        except Exception as e:
            print(f"Failed to check if extension is enabled via D-Bus: {e}")
        return extension_id in self._get_enabled_extensions_fallback()

    def enable_extension(self, extension_id):
        """Enable an extension"""
        if not self._proxy:
            return False
        try:
            if hasattr(self._proxy, "EnableExtension"):
                self._proxy.EnableExtension('(s)', extension_id)
            elif hasattr(self._proxy, "call_sync"):
                self._proxy.call_sync(
                    "EnableExtension",
                    GLib.Variant("(s)", (extension_id,)),
                    Gio.DBusCallFlags.NONE,
                    -1,
                    None
                )
            print(f"Enabled extension: {extension_id}")
            return True
        except Exception as e:
            print(f"Error enabling extension {extension_id}: {e}")
            return False

    def disable_extension(self, extension_id):
        """Disable an extension"""
        if not self._proxy:
            return False
        try:
            if hasattr(self._proxy, "DisableExtension"):
                self._proxy.DisableExtension('(s)', extension_id)
            elif hasattr(self._proxy, "call_sync"):
                self._proxy.call_sync(
                    "DisableExtension",
                    GLib.Variant("(s)", (extension_id,)),
                    Gio.DBusCallFlags.NONE,
                    -1,
                    None
                )
            print(f"Disabled extension: {extension_id}")
            return True
        except Exception as e:
            print(f"Error disabling extension {extension_id}: {e}")
            return False

    def toggle_extension(self, extension_id):
        """Toggle extension state"""
        if self.is_extension_enabled(extension_id):
            return self.disable_extension(extension_id)
        else:
            return self.enable_extension(extension_id)

    def is_extension_installed(self, extension_id):
        # Check user and system extension directories
        user_dir = os.path.expanduser("~/.local/share/gnome-shell/extensions")
        system_dir = "/usr/share/gnome-shell/extensions"
        for base in [user_dir, system_dir]:
            if os.path.isdir(base):
                for ext in os.listdir(base):
                    if ext == extension_id:
                        return True
        return False

    def get_sorted_extensions(self):
        """Get extensions sorted by installation status (installed first)"""
        extensions = self.get_extensions()
        installed = []
        not_installed = []

        for extension in extensions:
            if self.is_extension_installed(extension['id']):
                installed.append(extension)
            else:
                not_installed.append(extension)

        return installed + not_installed