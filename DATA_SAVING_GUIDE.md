# DATA_SAVING_GUIDE.md — Veri Kaydetme Rehberi

Bu belge, ParsLinux GNOME Greeter'ın **kullanıcı tercihlerini nasıl ve nerede
sakladığını** açıklar. Geliştiricilerin yeni ayar eklerken uyması gereken
kuralları içerir.

## Nerede Saklanır?

Uygulamanın kendi durumu **GSettings** üzerinden saklanır:

- **Şema:** `org.parslinux.parslinux-gnome-greeter`
  (tanım: `data/schemas/org.parslinux.parslinux-gnome-greeter.gschema.xml`)
- **Arşiv konumu:** kurulumda `/usr/share/glib-2.0/schemas/`, derleme sonrası
  `build/data/schemas/` altında derlenmiş `.compiled` dosya.
- **Kullanıcı değeri:** `~/.config/dconf/user` (dconf backend).

Komut satırından incelemek için:

```bash
gsettings list-recursively org.parslinux.parslinux-gnome-greeter
gsettings get org.parslinux.parslinux-gnome-greeter <anahtar>
```

## Sistem Ayarları

Uygulama ayrıca doğrudan GNOME şemalarına yazar (kullanıcı deneyimini kalıcı
kılan asıl ayarlar bunlardır):

| Şema | Ne için | Manager |
|---|---|---|
| `org.gnome.desktop.interface` | tema, ikon, font, ölçek | ThemeManager / DisplayManager |
| `org.gnome.desktop.background` | duvar kağıdı yolu | WallpaperManager |
| `org.gnome.shell` | etkin eklenti listesi | ExtensionManager |
| `org.gnome.desktop.wm.keybindings` | özel kısayollar | ShortcutManager |

## Yeni Bir Ayar Anahtarı Ekleme Adımları

1. `data/schemas/*.gschema.xml` dosyasına `<key>` tanımı ekle
   (`type`, `default`, gerekirse `summary`/`description`).
2. `glib-compile-schemas` yeniden çalışır (Meson hedefi otomatik); yine de
   yerelde test için: `glib-compile-schemas data/schemas`.
3. Kod tarafında `app_settings.set("anahtar", değer)` / `.get(...)` kullan —
   **doğrudan Gio.Settings'e dokunma**, `managers/settings.py` sarmalayıcısını kullan.
4. `set()` tipi otomatik algılar: mevcut anahtarın GVariant tip string'i alınır;
   bu yüzden default tipten farklı tipte yazmaya çalışma (`as` tipi için
   `set_strv` kullan).
5. Test ekle: `tests/test_settings_manager.py` içindeki `FakeSettings` kalıbı
   yeni anahtarı da içermeli.

## İndirilen Dosyalar (Duvar Kağıtları vb.)

- İndirme hedefi: `~/.local/share/parslinux-gnome-greeter/` altında tutulur
  (kaynak listesi: `data/json/wallpaper_sources.json`).
- Yollar GSettings'teki string/string-array anahtarlarında saklanır.
- Silme/kaldırma senaryosunda önce dconf anahtarı temizlenmeli, sonra dosya
  silinmeli (kopuk referans kalmasın).

## Bozulmaya Karşı Kurallar

- **Asla** anahtar adı değiştirip eski veriyi yetim bırakma; taşıma gerekiyorsa
  açılışta eski→yeni kopyalama migrasyonu ekle.
- JSON katalog dosyaları salt-okunur veri kaynağıdır; kullanıcı girişi oraya
  yazılmaz, kullanıcı override'ları GSettings'e yazılır.
- Hatalı anahtara `set()` istisna fırlatmaz, `False` döner (test edilmiştir);
  çağıran taraf sonucu kontrol etmeli.
