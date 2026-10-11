#!/usr/bin/env bash
# install.sh — ParsLinux GNOME Greeter uygulamasını kaynaktan kurar.
# Desteklenen paket yöneticileri: pacman (Arch), apt (Debian/Ubuntu), dnf (Fedora)
# Kullanım: sudo ./install.sh [--prefix /usr/local] [--no-deps]
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

PREFIX="/usr/local"
INSTALL_DEPS=true
BUILD_DIR="$PROJECT_ROOT/build"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prefix) PREFIX="$2"; shift 2 ;;
        --no-deps) INSTALL_DEPS=false; shift ;;
        -h|--help)
            echo "Kullanım: $0 [--prefix <yol>] [--no-deps]"
            echo "  --prefix : Kurulum hedefi (varsayılan: /usr/local)."
            echo "             Arch Linux için önerilen: /usr"
            echo "  --no-deps: Bağımlılık kurulumunu atla."
            exit 0
            ;;
        *) echo "Bilinmeyen seçenek: $1"; exit 1 ;;
    esac
done

SUDO=""
if [[ $EUID -ne 0 ]]; then
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        echo "HATA: Root yetkisi gerekiyor (sudo da yok). 'su -' ile root olarak çalıştırın."
        exit 1
    fi
fi

# --- 1. Bağımlılıkları tespit et ve kur ------------------------------------
detect_pkg_manager() {
    if command -v pacman >/dev/null 2>&1; then echo "pacman"
    elif command -v apt-get >/dev/null 2>&1; then echo "apt"
    elif command -v dnf >/dev/null 2>&1; then echo "dnf"
    elif command -v zypper >/dev/null 2>&1; then echo "zypper"
    else echo "unknown"
    fi
}

PKG_MGR="$(detect_pkg_manager)"
echo "==> Tespit edilen paket yöneticisi: $PKG_MGR"

install_deps() {
    case "$PKG_MGR" in
        pacman)
            # Arch Linux bağımlılıkları
            $SUDO pacman -S --needed --noconfirm \
                python python-gobject gtk4 libadwaita glib2 \
                meson ninja gettext desktop-file-utils shared-mime-info
            ;;
        apt)
            $SUDO apt-get update
            $SUDO apt-get install -y \
                python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 \
                libgtk-4-dev libadwaita-1-dev libglib2.0-dev-bin \
                meson ninja-build gettext pkg-config \
                desktop-file-utils shared-mime-info
            ;;
        dnf)
            $SUDO dnf install -y \
                python3 python3-gobject gtk4 libadwaita glib2-devel \
                meson ninja-build gettext pkgconfig \
                desktop-file-utils shared-mime-info
            ;;
        zypper)
            $SUDO zypper install -y \
                python3 python3-gobject typelib-1_0-Gtk-4_0 typelib-1_0-Adw-1 \
                gtk4-devel libadwaita-devel glib2-devel \
                meson ninja gettext desktop-file-utils
            ;;
        *)
            echo "UYARI: Bilinmeyen paket yöneticisi. Lütfen şu paketleri elle kurun:"
            echo "  python3, PyGObject (gi), GTK4, LibAdwaita, glib-compile-resources,"
            echo "  meson, ninja, gettext"
            ;;
    esac
}

if $INSTALL_DEPS; then
    echo "==> Bağımlılıklar kuruluyor..."
    install_deps
else
    echo "==> Bağımlılık kurulumu atlandı (--no-deps)."
fi

# --- 2. Zorunlu araç kontrolü -------------------------------------------------
for tool in python3 meson ninja glib-compile-resources msgfmt; do
    command -v "$tool" >/dev/null 2>&1 || {
        echo "HATA: '$tool' bulunamadı. Bağımlılık kurulumunu tekrar deneyin (--no-deps kullanmayın)."
        exit 1
    }
done

# --- 3. Meson ile derle ve kur ------------------------------------------------
echo "==> Meson yapılandırması (prefix=$PREFIX)"
if [[ ! -f "$BUILD_DIR/build.ninja" ]]; then
    meson setup "$BUILD_DIR" --prefix="$PREFIX" --reconfigure || \
        meson setup "$BUILD_DIR" --prefix="$PREFIX"
fi

echo "==> Derleme"
ninja -C "$BUILD_DIR"

echo "==> Kurulum"
$SUDO ninja -C "$BUILD_DIR" install

# --- 4. Kurulum sonrası işlemler ----------------------------------------------
SCHEMA_DIR="$PREFIX/share/glib-2.0/schemas"
if [[ -d "$SCHEMA_DIR" ]] && ls "$SCHEMA_DIR"/org.parslinux.*.gschema.xml >/dev/null 2>&1; then
    echo "==> GSettings şemaları derleniyor"
    $SUDO glib-compile-schemas "$SCHEMA_DIR"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
    $SUDO update-desktop-database "$PREFIX/share/applications" 2>/dev/null || true
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    for d in "$PREFIX"/share/icons/*; do
        [[ -d "$d" ]] && gtk-update-icon-cache -q -t -f "$d" 2>/dev/null || true
    done
fi

echo ""
echo "=================================================="
echo " Kurulum tamamlandı!"
echo "   Uygulama : parslinux-gnome-greeter"
echo "   Prefix   : $PREFIX"
echo "   Çalıştır : parslinux-gnome-greeter"
echo "=================================================="
