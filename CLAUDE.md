# CLAUDE.md — AI Asistanı Rehberi

Bu dosya, bu depoda çalışan yapay zekâ asistanları (Claude vb.) için bağlam ve kuralları içerir.

## Proje Özeti

**ParsLinux GNOME Greeter**, ParsLinux kurulumundan sonraki ilk oturum açılışta çalışan bir "kurulum sonrası sihirbaz" (welcome tour) uygulamasıdır. GTK4 + LibAdwaita tabanlıdır; Python 3 ile yazılmıştır ve Meson ile derlenir.

- **Uygulama kimliği:** `org.parslinux.parslinux-gnome-greeter`
- **Dil:** Kod yorumları ve commit mesajları dahil proje dili Türkçe/İngilizce karışık; yeni dokümanlarda Türkçe tercih edilir.
- **Marka:** Tüm metinlerde **Pardus değil, ParsLinux** kullanılmalıdır (marka temizliği tamamlandı, geriye kaçmasına izin verme).

## Dizin Yapısı

```
src/parslinux_gnome_greeter/   # Ana Python paketi
  main_window.py               # Adw.ApplicationWindow + SplitView ana pencere
  pages/                       # Her sihirbaz adımı ayrı sınıf (welcome, theme, wallpaper...)
  managers/                    # Sistem mantığı (GSettings, dbus, dosya işlemleri)
  components/                  # AboutDialog gibi ortak bileşenler
data/
  ui/                          # .ui (GtkBuilder) dosyaları
  json/                        # Veri tanımları (eklentiler, kısayollar, duvar kağıtları...)
  schemas/                     # GSettings şeması
  po/                          # Çeviriler (tr, es, pt)
  assets/ icons/ css/ autostart/
tests/                         # pytest testleri (gi sahte/stub ile izole)
debian/                        # Debian paketleme
```

## Çalıştırma & Test

```bash
# Derleme/kurulum (INSTALL.md'ye bakın)
meson setup build && meson compile -C build

# Testler (GTK olmadan da çalışır — conftest.py gi'yi stub'lar)
python -m pytest
```

## Kurallar

1. **Testleri bozma:** `python -m pytest` her değişiklikten sonra geçmeli (29 test).
2. **GSettings anahtarları:** Şemayı (`data/schemas/*.gschema.xml`) değiştirdiysen hem `SettingsManager` kullanımını hem testleri güncelle.
3. **UI değişiklikleri:** `.ui` dosyaları ile Python kodu senkron olmalı; `gresource.xml` listesini güncellemeyi unutma.
4. **Çeviri:** Yeni kullanıcıya dönük string eklersen `data/po/*.po` ve `.pot` dosyalarını da güncelle (`./update-translations.sh`).
5. **Dosya isimleri:** Mevcut `CamelCase` manager dosyaları geçmişten geliyor; yeni dosyalarda PEP8 (`snake_case`) kullan.
6. **Commit mesajları:** Ne değiştiğini net anlatan kısa İngilizce veya Türkçe mesajlar yaz.
7. **Lisans:** GPL-3.0; dosyaların başındaki lisans başlıklarını koru.

## Bilinen Tuzaklar

- `managers/settings.py` import anında `Gio.Settings.new()` çağırır; modülü izole test etmek için `tests/test_settings_manager.py`'deki `importlib` + monkeypatch kalıbını kullan.
- Uygulama gerçek sistem ayarlarını değiştirir; testlerde asla gerçek GSettings'e yazma (conftest bunu stub'lar).
- `pydbus` eklenti yönetimi (`ExtensionManager`) için gerekir; ortamda yoksa conftest sahte modül enjekte eder.
