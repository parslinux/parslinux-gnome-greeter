# Changelog

Bu proje için önemli değişiklikler burada belgelenir.

Biçim [Keep a Changelog](https://keepachangelog.com/tr/1.1.0/) temellidir ve
proje [Sürümleme](VERSION.md) kurallarına uyar.

## [Yayınlanmamış]

### Eklendi
- pytest tabanlı test altyapısı (`tests/`): SettingsManager, LayoutManager,
  veri dosyası bütünlüğü, appinfo, sayfa kaydı ve arayüz testleri (34 test, gi/pydbus stub'larıyla başlessız çalışır)
- Arch Linux desteği: `run.sh`, `install.sh`, `uninstall.sh` betikleri ve `PKGBUILD`;
  `meson.build`de site-packages hedefinin otomatik tespiti
- Dokümantasyon: `docs/` klasörü altında `INSTALL.md`, `ARCHITECTURE.md`,
  `VERSION.md`, `progress.md`, `DATA_SAVING_GUIDE.md`, `SELF_HOSTING_GUIDE.md`,
  `PAYMENT_INTEGRATION.md`, `UYGULAMA_BAGLAMA.md`, `TESTING.md`, `CONTRIBUTING.md`
  ve kök dizinde AI asistan dosyaları (`CLAUDE.md`, `.claudeignore`)

### Değiştirildi
- Modüller PEP 8 (`snake_case`) adlandırmasına taşındı (`managers/` ve `components/`),
  eski `CamelCase.py` modülleri geriye dönük uyumluluk katmanı (shim) olarak korundu
- Tüm dokümantasyon `.md` dosyaları kök dizinden `docs/` klasörüne taşındı
  (README.md ve CLAUDE.md kökte kaldı)
- Marka temizliği: tüm "Pardus" referansları "ParsLinux" ile değiştirildi
  (uygulama kimliği `org.parslinux.parslinux-gnome-greeter`, dosya adları,
  GSettings şeması, desktop/autostart dosyaları ve kullanıcı metinleri)

## [0.0.13]
- Upstream (pardus-setup-tour) son yayınlanan sürüm; yeniden markalama öncesi temel.
