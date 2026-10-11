#!/usr/bin/env bash
# PKGBUILD — ParsLinux GNOME Greeter için Arch Linux paketi.
# Kullanım:
#   makepkg -si            # derle + bağımlılıkları kur + paketle
# veya dizini bir arşive alıp:
#   updpkgsums && makepkg --printsrcinfo > .SRCINFO
pkgname=parslinux-gnome-greeter
pkgver=0.0.13
pkgrel=1
pkgdesc="Pars Linux kurulum sonrası yapılandırma sihirbazı (welcome tour)"
arch=('any')
url="https://github.com/parslinux/parslnux-gnome-greeter"
license=('GPL3')
depends=(
    'python'
    'python-gobject'
    'gtk4'
    'libadwaita'
    'glib2'
)
makedepends=('meson' 'ninja' 'gettext' 'desktop-file-utils')
optdepends=(
    'gnome-shell: GNOME masaüstü entegrasyonu'
)
source=("git+${url}.git#branch=master")
sha256sums=('SKIP')

build() {
    cd "$srcdir/${pkgname}" || cd "$srcdir/parslnux-gnome-greeter"
    meson setup build --prefix /usr
    ninja -C build
}

package() {
    cd "$srcdir/${pkgname}" || cd "$srcdir/parslnux-gnome-greeter"
    DESTDIR="$pkgdir" ninja -C build install
    [[ -f LICENSE ]] && install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
