# VERSION.md — Sürüm Yönetimi

## Geçerli Sürüm

**0.0.13** (kaynak: `meson.build` içindeki `version:` alanı)

## Sürüm Numaralandırma Şeması

Proje `MAJOR.MINOR.PATCH` formatını kullanır:

- **MAJOR:** Uygulama kimliği/veri formatında geriye uyumsuz değişiklik (ör. GSettings şeması kırılması)
- **MINOR:** Yeni sayfa, yeni manager, yeni özellik
- **PATCH:** Hata düzeltme, çeviri güncellemesi, marka/doküman düzeltmesi

## Sürüm Yükseltme Kontrol Listesi

1. `meson.build` → `version: 'X.Y.Z'` güncelle
2. `CHANGELOG.md` → yeni sürüm başlığı ve girdileri ekle
3. `org.parslinux.parslinux-gnome-greeter.appdata.xml.in` (kök dizin) → `<release version="X.Y.Z" date="YYYY-MM-DD"/>` satırı ekle
4. `debian/changelog` → `debchange -v X.Y.Z` veya elle girdi (ParsLinux dağıtım sürümüyle uyumlu hedef)
5. Commit: `Release X.Y.Z` → etiketle: `git tag -a vX.Y.Z -m "..."`

## Dağıtım Kanalları

| Kanal | Kaynak | Not |
|---|---|---|
| ParsLinux depo | `debian/` paketinden üretilen .deb | İmzalı, autostart dahil |
| GitHub Release | `vX.Y.Z` etiketi + kaynak tarball | Meson ile derlenebilir |
| Flatpak (planlandı) | — | Henüz manifest yok; bkz. CHANGELOG yol haritası |

## Uyumluluk

- GTK ≥ 4.10, libadwaita ≥ 1.4 gerektirir.
- GNOME Shell eklenti API'si sürümler arası kırıcı olabildiğinden
  `data/json/extensions.json` içindeki `shell_version` kısıtları her GNOME
  büyük sürümünde gözden geçirilmelidir.
