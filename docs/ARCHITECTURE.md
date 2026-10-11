# ARCHITECTURE.md — ParsLinux GNOME Greeter Mimari Rehberi

## Genel Bakış

Uygulama, **katmanlı bir mimari** izler: UI sayfaları ince kalır, tüm sistem
etkileşimi "Manager" sınıflarına devredilir. Böylece manager'lar GTK olmadan
da test/başka betiklerde yeniden kullanılabilir.

```
┌─────────────────────────────────────────────┐
│  main_window.py (Adw.ApplicationWindow)     │
│  SplitView + Sidebar (Gtk.ListBox)          │
│  ┌───────────────┐  ┌────────────────────┐  │
│  │ Navigation    │  │ Adw.ViewStack      │  │
│  │ (sayfa listesi)│──│ pages/* (her adım)  │  │
│  └───────────────┘  └─────────┬──────────┘  │
│                               │             │
│                    managers/* │             │
│                      (GSettings/dbus/fs)    │
└─────────────────────────────────────────────┘
```

## Katmanlar

### 1. Giriş Noktası
- `parslinux-gnome-greeter.in` → `src/parslinux_gnome_greeter/__main__.py`
- `Adw.Application` oluşturur, `main_window.MainWindow`'ı gösterir.
- Autostart dosyası (`data/autostart/`) sayesinde ilk oturum açılışta çalışır.

### 2. Ana Pencere (`main_window.py`)
- `Adw.SplitView`: geniş ekranda kenar çubuğu + içerik, dar ekranda tek görünüm.
- `Adw.ViewStack`: sayfalar arası geçiş; `Gtk.ListBox` navigasyonu sürer.
- Sayfalar kayıt sırasına göre ilerleme (progress) göstergesine bağlanır.

### 3. Sayfalar (`pages/`)
Her sihirbaz adımı kendi sınıfıdır:

| Sayfa | Sorumluluk |
|---|---|
| `welcome.py` | Karşılama, marka tanıtımı |
| `wallpaper.py` | Duvar kağıdı galerisi/indirme → `WallpaperManager` |
| `theme.py` | Açık/koyu tema, ikon/font teması → `ThemeManager` |
| `extension.py` | GNOME Shell eklenti önerileri → `ExtensionManager` |
| `layout.py` | Panel/düzen ayarları → `LayoutManager` |
| `display.py` | Ölçeklendirme/ekran → `DisplayManager` |
| `applications.py` | Önerilen uygulamalar, kısayollar → `ShortcutManager` |
| `time.py` | Saat/ülke/tarih biçimi |
| `outro.py` | Kapanış, tamamlanma işareti |

Sayfalar `.ui` dosyalarını `data/ui/` altından yükler (GtkBuilder).

### 4. Manager'lar (`managers/`)
Sistemle konuşan tek yer burasıdır:

- **`settings.py` → `SettingsManager`**: GSettings sarmalayıcı. Modül düzeyinde
  hazır örnekler kurulur: `app_settings` (uygulamanın kendi şeması),
  `theme_settings`, `shell_settings`, `background_settings`.
- **`WallpaperManager`**: duvar kağıdı kaynaklarını `data/json/wallpaper_sources.json`
  üzerinden indirir, `org.gnome.desktop.background`'a uygular.
- **`ThemeManager`**: `org.gnome.desktop.interface` üzerinden gtk/icon/font/cursor temaları.
- **`ExtensionManager`**: `pydbus` ile GNOME Shell D-Bus API'sinden eklenti listeler/etkinleştirir;
  öneriler `data/json/extensions.json`.
- **`LayoutManager`**: `data/json/layout_config.json` tabanlı panel düzeni.
- **`ShortcutManager`**: `data/json/shortcuts.json` ve `custom_shortcuts.json`.
- **`DisplayManager`**: ölçek/dpi ayarları.

### 5. Veri Katmanı (`data/`)
- `json/`: tüm öneri/katalog verisi (kod değişikliği gerektirmeden güncellenebilir).
- `schemas/org.parslinux.parslinux-gnome-greeter.gschema.xml`: uygulama durumu
  (tamamlanan sayfalar, seçilen duvar kağıdı vb.).
- `po/`: tr, es, pt çevirileri; `update-translations.sh` ile POT yenilenir.

## Bağımlılıklar

Python 3 • PyGObject (GTK4, libadwaita, Gio/GLib) • pydbus • Meson + glib-compile-schemas / compile-resources

## Test Stratejisi

`tests/conftest.py`, `gi` ve `pydbus` yoksa **sahte (stub) modüller** enjekte
eder; böylece manager mantığı başlessız ortamda (CI dahil) çalışır:

- `test_settings_manager.py` — SettingsManager'ı `FakeSettings/FakeVariant` ile izole test eder
- `test_layout_manager.py` — layout JSON şeması ve seçim mantığı
- `test_data_files.py` — tüm JSON'ların geçerliliği, `.ui` XML'lerinin geçerliliği, şema ID kontrolü

Çalıştırma: `python -m pytest`

## Tasarım İlkeleri

1. Sayfalar asla doğrudan GSettings yazmaz → her zaman manager kullanır.
2. Yeni sayfa eklemek = `pages/`e sınıf + `data/ui/`ye .ui + ViewStack kaydı.
3. Kullanıcı metinleri çevrilebilir olmalı (`_()` / translation.py).
4. Marka adı her zaman **ParsLinux**.
