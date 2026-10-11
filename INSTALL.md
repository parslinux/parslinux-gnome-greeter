# ParsLinux GNOME Greeter - Kurulum Rehberi (Installation Guide)

ParsLinux GNOME Greeter, kurulum sonrası ilk oturum açılışta çalışan, duvar kağıdı, tema, düzen ve ekran ayarlarını kolayca özelleştirmenizi sağlayan bir "hoş geldiniz" sihirbazıdır.

## Gereksinimler (Requirements)

| Bileşen | Sürüm |
|---|---|
| Python 3 | >= 3.6 |
| GTK4 + LibAdwaita | PyGObject üzerinden |
| Meson | >= 0.60.0 |
| glib-compile-tools (glib2-devel) | GResource derleme için |
| GNOME Shell | >= 40 |
| python3-pydbus | DBus etkileşimi için |
| gettext | Çeviri dosyaları (`.po`) için |

### Debian/Ubuntu tabanlı sistemlerde bağımlılıklar

```bash
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 \
    libadwaita-1-dev meson ninja-build libglib2.0-dev \
    python3-pydbus gettext
```

### Fedora tabanlı sistemlerde bağımlılıklar

```bash
sudo dnf install python3 python3-gobject gtk4-devel libadwaita-devel \
    meson ninja-build glib2-devel python3-pydbus gettext
```

## Kaynaktan Kurulum (Meson ile)

```bash
# Depoyu klonlayın
git clone https://github.com/parslinux/parslnux-gnome-greeter.git
cd parslinux-gnome-greeter

# Yapılandırma ve derleme
meson setup builddir --prefix=/usr
meson compile -C builddir

# Kurulum
sudo meson install -C builddir
```

Kurulum yapılan başlıca konumlar:

- Uygulama verileri: `/usr/share/parslinux/parslinux-gnome-greeter/`
- Python paketi: `/usr/lib/python3/dist-packages/parslinux_gnome_greeter/`
- Çalıştırılabilir: `/usr/bin/parslinux-gnome-greeter`
- Autostart (ilk oturumda otomatik başlatma): `/etc/xdg/autostart/org.parslinux.parslinux-gnome-greeter-autostart.desktop`
- Masaüstü dosyası ve ikonlar: `/usr/share/applications/`, `/usr/share/icons/hicolor/`

## Debian Paketi ile Kurulum

Depo kökündeki `debian/` dizini paketlemeye hazırdır:

```bash
# Bağımlılıkları kurun
sudo apt build-dep . 2>/dev/null || sudo apt install debhelper-compat=13 \
    dh-python meson libglib2.0-dev python3-setuptools

# .deb paketini üretin
dpkg-buildpackage -us -uc -b

# Paketleyip kurun
sudo dpkg -i ../parslinux-gnome-greeter_*.deb
```

## Doğrulama

```bash
# Uygulamayı elle çalıştırarak test edin
parslinux-gnome-greeter
```

Uygulama penceresi açılmazsa şunları kontrol edin:

1. `glib-compile-schemas` ile şemaların derlendiğinden emin olun:
   ```bash
   sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
   ```
2. `python3 -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1'); from gi.repository import Gtk, Adw"` komutunun hata vermediğini doğrulayın.

## Kaldırma

```bash
# Elle (meson) kurulumunda ilgili dosyaları kaldırın
sudo rm -rf /usr/share/parslinux/parslinux-gnome-greeter \
            /usr/lib/python3/dist-packages/parslinux_gnome_greeter \
            /usr/bin/parslinux-gnome-greeter \
            /etc/xdg/autostart/org.parslinux.parslinux-gnome-greeter-autostart.desktop \
            /usr/share/applications/org.parslinux.parslinux-gnome-greeter.desktop

# Debian paketiyle kurulumda
sudo apt remove parslinux-gnome-greeter
```

## Notlar

- Uygulama `org.parslinux.parslinux-gnome-greeter` uygulama kimliği (application ID) ile çalışır; GSettings şemaları da bu kimliğe göredir.
- İlk oturumda otomatik başlatma `data/autostart/` içindeki `.desktop` dosyası ile sağlanır; devre dışı bırakmak için dosyayı kaldırmanız yeterlidir.

## Arch Linux

### Seçenek 1: Betiklerle (hızlı)
```bash
sudo pacman -S --needed python python-gobject gtk4 libadwaita glib2 meson ninja gettext
./install.sh --prefix /usr        # kurulum
parslinux-gnome-greeter           # çalıştırma
sudo ./uninstall.sh --prefix /usr # kaldırma
```

### Seçenek 2: PKGBUILD ile (paket olarak)
```bash
makepkg -si    # derle + bağımlılıkları kur + paketle
```

### Geliştirme modu
```bash
./run.sh            # kaynak kodundan doğrudan çalıştır (gresource'u otomatik derler)
./run.sh --build    # data/ değiştiyse gresource'u yeniden derle
./run.sh --meson    # meson/ninja ile tam derleyip build/ üzerinden çalıştır
```
