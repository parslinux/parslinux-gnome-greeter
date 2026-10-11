# Changelog

Bu proje için önemli değişiklikler burada belgelenir.

Biçim [Keep a Changelog](https://keepachangelog.com/tr/1.1.0/) temellidir ve
proje [Sürümleme](VERSION.md) kurallarına uyar.

## [Yayınlanmamış]

### Eklendi
- pytest tabanlı test altyapısı (`tests/`): SettingsManager, LayoutManager ve
  veri dosyası bütünlük testleri (29 test, gi/pydbus stub'larıyla başlessız çalışır)
- `INSTALL.md`, `ARCHITECTURE.md`, `VERSION.md`, `progress.md` ve AI asistan
  dosyaları (`CLAUDE.md`, `.claudeignore`)
- Dokümantasyon rehberleri: `DATA_SAVING_GUIDE.md`, `SELF_HOSTING_GUIDE.md`,
  `PAYMENT_INTEGRATION.md`, `UYGULAMA_BAGLAMA.md`, `TESTING.md`, `CONTRIBUTING.md`

### Değiştirildi
- Marka temizliği: tüm "Pardus" referansları "ParsLinux" ile değiştirildi
  (uygulama kimliği `org.parslinux.parslinux-gnome-greeter`, dosya adları,
  GSettings şeması, desktop/autostart dosyaları ve kullanıcı metinleri)

## [0.0.13]
- Upstream (pardus-setup-tour) son yayınlanan sürüm; yeniden markalama öncesi temel.
