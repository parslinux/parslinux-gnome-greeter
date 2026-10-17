from ..appinfo import APP_ID

try:
    from gi.repository import Gio, GLib
except ImportError:
    # GLib, bazı ortamlarda (ör. test iskeletlerinde) ayrı bir tip modülü
    # olarak bulunmayabilir; Gio tek başına yeterliyse GLib'i ayrıca dene.
    from gi.repository import Gio
    try:
        from gi.repository import GLib
    except ImportError:
        GLib = None


class SettingsManager:
    def __init__(self, schema_id):
        self.schema_id = schema_id
        self.settings = None
        self._init_settings(schema_id)

    def _init_settings(self, schema_id):
        """Initializes Gio.Settings safely if schema is present on system."""
        try:
            if hasattr(Gio, "SettingsSchemaSource") and hasattr(Gio.SettingsSchemaSource, "get_default"):
                source = Gio.SettingsSchemaSource.get_default()
                if source is not None and not source.lookup(schema_id, True):
                    # Schema is not installed on this system
                    self.settings = None
                    return
            self.settings = Gio.Settings.new(schema_id)
        except Exception as e:
            self.settings = None

    def is_available(self):
        """Returns True if the underlying GSettings schema is available and loaded."""
        return self.settings is not None

    def get(self, key):
        """Gets a setting value. Returns None silently if key or schema is not available."""
        if self.settings is None:
            return None
        try:
            if hasattr(self.settings, "list_keys") and not self.settings.list_keys().__contains__(key):
                return None
            val = self.settings.get_value(key)
            return val.unpack() if hasattr(val, "unpack") else val
        except Exception as e:
            print(f"Warning: could not read setting '{key}': {e}")
            return None

    def get_safe(self, key, default=None):
        """Gets a setting value with a fallback default."""
        value = self.get(key)
        return value if value is not None else default

    def get_strv(self, key):
        """Gets a string array value."""
        if self.settings is None:
            return []
        try:
            if hasattr(self.settings, "list_keys") and not self.settings.list_keys().__contains__(key):
                return []
            return list(self.settings.get_strv(key))
        except Exception as e:
            print(f"Warning: could not read strv setting '{key}': {e}")
            return []

    def set(self, key, value):
        """Sets a setting value safely. Returns False if key or schema is missing."""
        if self.settings is None:
            return False
        try:
            if hasattr(self.settings, "list_keys") and not self.settings.list_keys().__contains__(key):
                return False

            original_variant = self.settings.get_value(key)
            type_string = original_variant.get_type_string()

            if GLib and hasattr(GLib, "Variant"):
                new_variant = GLib.Variant(type_string, value)
            else:
                new_variant = value

            return bool(self.settings.set_value(key, new_variant))
        except Exception as e:
            print(f"Error setting {key} = {value}: {e}")
            return False

    def set_strv(self, key, value):
        """Sets a string array value safely."""
        if self.settings is None:
            return False
        try:
            if hasattr(self.settings, "list_keys") and not self.settings.list_keys().__contains__(key):
                return False
            return bool(self.settings.set_strv(key, value))
        except Exception as e:
            print(f"Error setting strv {key} = {value}: {e}")
            return False


# Application specific settings
app_settings = SettingsManager(APP_ID)

# GNOME Desktop Interface settings (for themes, fonts, etc.)
theme_settings = SettingsManager("org.gnome.desktop.interface")

# GNOME Shell settings
shell_settings = SettingsManager("org.gnome.shell")

# GNOME Desktop Background settings
background_settings = SettingsManager("org.gnome.desktop.background")