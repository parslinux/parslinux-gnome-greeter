# progress.md — Proje İlerleme Durumu

**Son güncelleme:** 2026-10-11

## Tamamlananlar

### ✅ Marka Yenileme (Pardus → ParsLinux)
- Uygulama kimliği: `org.parslinux.parslinux-gnome-greeter` (commit `664d28b`)
- Dosya adları, GSettings şeması, desktop/autostart/appdata dosyaları dönüştürüldü
- Kalan tüm Pardus referansları temizlendi (commit `f203e88`)
- Korunan istisnalar: geçmiş changelog girdileri, geliştirici e-posta adresleri, SVG logolar

### ✅ Test Altyapısı (pytest)
- `pytest.ini` + `tests/` iskeleti kuruldu
- `tests/conftest.py`: gi/pydbus yoksa **stub enjeksiyonu** → başlessız test
- 3 test dosyası, **29/29 test geçiyor** (`python -m pytest`):
  - `test_settings_manager.py` — SettingsManager birim testleri (FakeSettings/FakeVariant; `GLib.Variant(type, value)` kalıbı dahil)
  - `test_layout_manager.py` — LayoutManager mantığı
  - `test_data_files.py` — JSON/UI/gschema bütünlük kontrolleri
- `settings.py` import'u GLib eksik ortamlara karşı dayanıklı hale getirildi
- Bozuk harici pytest eklentisi (libtmux) `pytest.ini`de `-p no:libtmux` ile devre dışı

### ✅ Dokümantasyon
| Dosya | İçerik |
|---|---|
| `INSTALL.md` | Gereksinimler, Meson kurulumu, Debian paketi, kaldırma |
| `ARCHITECTURE.md` | Katmanlar: pencere/sayfalar/manager'lar/veri, test stratejisi |
| `VERSION.md` | 0.0.13, numaralandırma şeması, sürüm kontrol listesi |
| `CHANGELOG.md` | Keep-a-Changelog formatında yayınlanmamış değişiklikler |
| `DATA_SAVING_GUIDE.md` | GSettings/dconf veri katmanı, anahtar ekleme kuralları |
| `SELF_HOSTING_GUIDE.md` | Kendi içerik sunucusu, air-gapped dağıtım |
| `PAYMENT_INTEGRATION.md` | Bağış/ödeme entegrasyonu yerleri ve GPL uyumu |
| `UYGULAMA_BAGLAMA.md` | Dağıtıma entegrasyon: autostart, şema, paket zinciri |
| `TESTING.md` | Test çalıştırma, yazma kuralları, CI önerisi |
| `CONTRIBUTING.md` | Katkı kuralları, PR akışı |
| `CLAUDE.md` / `.claudeignore` | AI asistanları için bağlam ve hariç tutmalar |

## Devam Eden / Sonraki Adımlar

- ⏳ Bu dokümantasyon + test değişikliklerinin **git commit**'lenmesi (son adım)
- 🔜 GitHub Actions CI workflow (build + pytest)
- 🔜 CamelCase manager dosyalarının snake_case'e taşınması (API bozmadan)
- 🔜 ExtensionManager/WallpaperManager için mock tabanlı ek testler
- 🔜 Çeviri dosyalarında marka metinlerinin gözden geçirilmesi

## Bilinen Notlar

- Uygulama hâlâ "greeter" adıyla anılıyor ancak teknik olarak kurulum sonrası
  sihirbazdır (login ekranı değildir); isimlendirme ileride değişebilir.
- Flatpak manifesti yok (VERSION.md'de planlandı olarak işaretli).
