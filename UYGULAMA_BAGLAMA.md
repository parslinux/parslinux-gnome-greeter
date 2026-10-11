# UYGULAMA_BAGLAMA.md — Uygulama Bağlama / Entegrasyon Rehberi

Bu belge, ParsLinux GNOME Greeter'ın **bir masaüstü ortamina/dağıtıma nasıl
bağlanacağını** (entegre edileceğini) adım adım anlatır: autostart, GSettings
şeması, desktop dosyası ve paket bütünlüğü.

## 1. Kimlikler (Naming Contract)

Her yerde aynı kimlik kullanılmalıdır; birini değiştirmek diğerlerini kırar:

| Öğe | Değer |
|---|---|
| Uygulama ID (Adw.Application) | `org.parslinux.parslinux-gnome-greeter` |
| GSettings schema ID | `org.parslinux.parslinux-gnome-greeter` |
| Desktop dosyası | `org.parslinux.parslinux-gnome-greeter.desktop` |
| Autostart dosyası | `data/autostart/` içindeki `.desktop` |
| gresource path | `/org/parslinux/parslinux-gnome-greeter/...` |
| Python paketi | `src/parslinux_gnome_greeter/` |

## 2. Derleme & Kurulum Zinciri (Meson)

```bash
meson setup build --prefix=/usr
meson compile -C build
sudo meson install -C build
```

`meson install` sırasında bağlanan parçalar:

1. **Şema derleme:** `data/schemas/` → `/usr/share/glib-2.0/schemas/` +
   `glib-compile-schemas` (debian install hedefinde de mevcut).
2. **GResource:** `parslinux-gnome-greeter.gresource.xml` derlenip ikili içine
   gömülür → UI/CSS/ikonlar tek dosyadan gelir.
3. **Desktop & ikonlar:** `/usr/share/applications/` ve `/usr/share/icons/`.
4. **Autostart:** `/etc/xdg/autostart/` — oturum açılışında sihirbazı başlatır.
5. **Launcher script:** `parslinux-gnome-greeter.in` → `@PYTHON@` ve enstalasyon
   yolu yerleştirilerek `/usr/bin/parslinux-gnome-greeter` olur.

## 3. Otomatik Başlatma Koşulu

Autostart `.desktop` dosyasında `X-GNOME-Autostart-Delay` ve uygulamanın kendi
"tamamlandı mı?" kontrolü birlikte çalışır: uygulama açılışta GSettings'teki
`completed` benzeri anahtara bakar; sihirbaz tamamlanmışsa sessizce çıkar.
Yeni bir dağıtıma bağlarken bu anahtarın sıfırlanma politikasını belirleyin
(ör. ISO testleri için `dconf reset -f /org/parslinux/parslinux-gnome-greeter/`).

## 4. Farklı Ortamlara Bağlama

### a) Saf GNOME (GNOME Shell)
Varsayıdan desteklenir; `ExtensionManager` D-Bus üzerinden shell'e bağlanır
(`org.gnome.Shell.Extensions`), bu yüzden **GNOME Shell etkin oturum** gerekir.

### b) Wayland / X11
Uygulama GTK4 olduğu için her ikisinde çalışır; Wayland'de pencere boyutu
algoritması (`SplitView` breakpoint'leri) farklı davranabilir — dar pencerelerde
test edin.

### c) Başka bir masaüstü (XFCE vb.)
GTK4/Adw bağımlılıkları kurulmalı; `org.gnome.*` şemaları bulunmadığından
ThemeManager/BackgroundSettings yazmaları sessiz başarısız olabilir. Böyle bir
ortama bağlarken ilgili sayfaları devre dışı bırakan bir "platform tespiti"
ekleyin (`GLib.getenv("XDG_CURRENT_DESKTOP")`).

## 5. Paket Üretimi (Debian)

```bash
dpkg-buildpackage -us -uc -b   # debian/ diziniyle
```

Bağlama noktaları: `debian/rules` meson'u çağırır, `debian/*.install`
autostart/desktop/şema dosyalarını paketler. Yeni dosya eklerseniz hem
`meson.build` install listesi hem `debian/install` güncellenmeli.

## 6. Sık Kırılan Bağlantılar (Kontrol Listesi)

- [ ] Şema ID ↔ `SettingsManager(schema_id)` birebir aynı mı?
- [ ] `.ui` dosyası eklendi mi → `gresource.xml`e yazıldı mı?
- [ ] Yeni sayfa → ViewStack + sidebar listesine eklendi mi?
- [ ] Çeviri gerekiyor mu → POT yenelendi mi (`./update-translations.sh`)?
- [ ] Autostart komutu `/usr/bin/parslinux-gnome-greeter` yolunu buluyor mu?
- [ ] Testler geçiyor mu → `python -m pytest`
