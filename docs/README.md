# Dokümantasyon

ParsLinux GNOME Greeter (kurulum sonrası yapılandırma sihirbazı) için tüm
rehberler bu klasörde toplanmıştır.

## Rehberler

| Dosya | İçerik |
|---|---|
| [INSTALL.md](INSTALL.md) | Gereksinimler, Meson ile kurulum, Arch Linux betikleri (`run.sh`, `install.sh`, `PKGBUILD`), Debian paketi, kaldırma |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Mimari katmanlar: pencere/sayfalar, manager'lar, veri dosyaları, test stratejisi |
| [VERSION.md](VERSION.md) | Sürüm numaralandırma şeması ve sürüm yükseltme kontrol listesi |
| [CHANGELOG.md](CHANGELOG.md) | Yayın geçmişi (Keep a Changelog biçimi) |
| [TESTING.md](TESTING.md) | Testleri çalıştırma/yazma kuralları, CI önerisi |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Katkı kuralları ve PR akışı |
| [DATA_SAVING_GUIDE.md](DATA_SAVING_GUIDE.md) | GSettings/dconf veri katmanı, yeni anahtar ekleme kuralları |
| [SELF_HOSTING_GUIDE.md](SELF_HOSTING_GUIDE.md) | Kendi içerik sunucunu barındırma, air-gapped dağıtım |
| [PAYMENT_INTEGRATION.md](PAYMENT_INTEGRATION.md) | Bağış/ödeme entegrasyonu noktaları ve GPL uyumu |
| [UYGULAMA_BAGLAMA.md](UYGULAMA_BAGLAMA.md) | Dağıtıma entegrasyon: autostart, gschema, paket zinciri |
| [progress.md](progress.md) | Proje ilerleme durumu (güncel iş kaydı) |

## Kök dizinde kalanlar

- [`../README.md`](../README.md) — proje tanıtımı
- [`../CLAUDE.md`](../CLAUDE.md) ve [`../.claudeignore`](../.claudeignore) —
  AI asistanları için bağlam dosyaları (araçlar tarafından otomatik keşfedilmeleri
  için kökte kalmalıdırlar)
