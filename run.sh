#!/usr/bin/env bash
# run.sh — ParsLinux GNOME Greeter uygulamasını geliştirme ortamında çalıştırır.
# Kullanım: ./run.sh [--build] [--meson]
#   --build : GResource dosyasını yeniden derle (data/ altında değişiklik yaptıysan)
#   --meson : Meson build dizinini kur ve oradan çalıştır (varsayılan: basit mod)
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

APP_NAME="parslinux-gnome-greeter"
GRESOURCE="${APP_NAME}.gresource"
GRESOURCE_XML="${APP_NAME}.gresource.xml"

REBUILD_RESOURCE=false
USE_MESON=false

APP_ARGS=()
for arg in "$@"; do
    case "$arg" in
        --build) REBUILD_RESOURCE=true ;;
        --meson) USE_MESON=true ;;
        -h|--help)
            echo "Kullanım: $0 [--build] [--meson] [uygulama_parametreleri...]"
            echo "  --build : GResource dosyasını yeniden derle"
            echo "  --meson : Meson ile tam kurulumdan sonra build dizininden çalıştır"
            exit 0
            ;;
        *) APP_ARGS+=("$arg") ;;
    esac
done

# --- Bağımlılık kontrolü ---------------------------------------------------
MISSING=()
command -v python3 >/dev/null 2>&1 || MISSING+=("python3")

if ! python3 -c "import gi" >/dev/null 2>&1; then
    MISSING+=("python-gobject (PyGObject)")
else
    if ! python3 - <<'EOF'
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw  # noqa
EOF
    then
        MISSING+=("GTK4 typelib (gir1.2-gtk-4.0 / gtk4) veya LibAdwaita typelib (gir1.2-adw-1 / libadwaita)")
    fi
fi

if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo "HATA: Eksik bağımlılıklar tespit edildi:"
    printf '  - %s\n' "${MISSING[@]}"
    echo ""
    echo "Arch Linux için kurulum önerisi:"
    echo "  sudo pacman -S --needed python python-gobject gtk4 libadwaita glib2"
    echo ""
    echo "Debian/Ubuntu tabanlı sistemler için:"
    echo "  sudo apt install python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libgtk-4-dev libadwaita-1-dev"
    exit 1
fi

# --- Mod: Meson ------------------------------------------------------------
if $USE_MESON; then
    command -v meson >/dev/null 2>&1 || {
        echo "HATA: meson bulunamadı. Arch: sudo pacman -S meson ninja"
        exit 1
    }
    BUILD_DIR="$PROJECT_ROOT/build"
    if [[ ! -f "$BUILD_DIR/build.ninja" ]]; then
        echo "==> Meson yapılandırması: $BUILD_DIR"
        meson setup "$BUILD_DIR"
    fi
    echo "==> Derleme (ninja)"
    ninja -C "$BUILD_DIR"
    echo "==> Çalıştırma: $BUILD_DIR/${APP_NAME}"
    exec "$BUILD_DIR/${APP_NAME}"
fi

# --- Mod: Basit (kaynak kodundan doğrudan) ---------------------------------
# Uygulama, gresource'u <proje_kökü>/build/parslinux-gnome-greeter.gresource
# yolundan arar (bkz. __main__.py). Bu yüzden çıktı build/ dizinine derlenir.
BUILD_DIR="$PROJECT_ROOT/build"
RES_TARGET="$BUILD_DIR/$GRESOURCE"

if $REBUILD_RESOURCE || [[ ! -f "$RES_TARGET" ]]; then
    if command -v glib-compile-resources >/dev/null 2>&1; then
        mkdir -p "$BUILD_DIR"
        echo "==> GResource derleniyor: $RES_TARGET"
        glib-compile-resources \
            --target="$RES_TARGET" \
            --sourcedir="$PROJECT_ROOT/data" \
            "$GRESOURCE_XML"
    else
        echo "UYARI: glib-compile-resources bulunamadı."
        echo "        'meson setup build && ninja -C build' ile derleyip tekrar deneyin."
    fi
fi

echo "==> Çalıştırılıyor (dev modu): $APP_NAME"
# ~/.local/share'i XDG_DATA_DIRS'a ekle — kullanıcı dizinine kurulan gschema
# değişikliklerinin (ör. custom-accent-color) gsettings tarafından görülmesi için.
XDG_DATA_DIRS="${HOME}/.local/share${XDG_DATA_DIRS:+:$XDG_DATA_DIRS}" \
PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" \
    exec python3 -m parslinux_gnome_greeter ${APP_ARGS[@]+"${APP_ARGS[@]}"}
