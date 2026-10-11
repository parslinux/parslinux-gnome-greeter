#!/usr/bin/env bash
# uninstall.sh — install.sh ile yapılan kurulumu kaldırır.
# Kullanım: sudo ./uninstall.sh [--prefix /usr/local]
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="/usr/local"
BUILD_DIR="$PROJECT_ROOT/build"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prefix) PREFIX="$2"; shift 2 ;;
        -h|--help) echo "Kullanım: $0 [--prefix <yol>]"; exit 0 ;;
        *) echo "Bilinmeyen seçenek: $1"; exit 1 ;;
    esac
done

SUDO=""
if [[ $EUID -ne 0 ]] && command -v sudo >/dev/null 2>&1; then SUDO="sudo"; fi

if [[ -f "$BUILD_DIR/install_log.txt" ]]; then
    echo "==> ninja uninstall çalıştırılıyor"
    $SUDO ninja -C "$BUILD_DIR" uninstall || {
        echo "UYARI: ninja uninstall başarısız, manuel silmeye düşülüyor."
    }
else
    echo "==> install_log.txt yok; bilinen yollar manuel siliniyor (prefix=$PREFIX)"
    $SUDO rm -rf "$PREFIX/share/parslinux/parslinux-gnome-greeter" \
             "$PREFIX/share/applications/org.parslinux.parslinux-gnome-greeter.desktop" \
             "$PREFIX/share/metainfo/org.parslinux.parslinux-gnome-greeter.appdata.xml" \
             "$PREFIX/share/glib-2.0/schemas/org.parslinux.parslinux-gnome-greeter.gschema.xml" \
             "$PREFIX/bin/parslinux-gnome-greeter" || true
fi

SCHEMA_DIR="$PREFIX/share/glib-2.0/schemas"
[[ -d "$SCHEMA_DIR" ]] && $SUDO glib-compile-schemas "$SCHEMA_DIR" || true

echo "==> Kaldırma tamamlandı."
