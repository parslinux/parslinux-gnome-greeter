# CONTRIBUTING.md — Katkı Rehberi

Katkılarınız için teşekkürler! ParsLinux GNOME Greeter'a katkı verirken bu
kurallara uymanız süreci hızlandırır.

## Başlamadan Önce

1. Depoyu fork'layın ve branch açın: `git checkout -b feat/yeni-ozellik`
2. Gerekli araçlar: Python 3, Meson, GTK4, libadwaita, PyGObject, pydbus, pytest
   (kurulum ayrıntıları: `INSTALL.md`)
3. Kod yazmadan önce mimariyi okuyun: `ARCHITECTURE.md`

## Geliştirme Döngüsü

```bash
meson setup build && meson compile -C build   # derleme
python -m pytest                               # testler (hepsi geçmeli!)
./update-translations.sh                       # çeviri POT yenileme (gerekirse)
```

## Kurallar

- **Marka:** her yerde **ParsLinux**; "Pardus" referansı bırakan PR geri döner.
- **Çevrilebilirlik:** yeni kullanıcı metni varsa `_()` ile sarın ve `data/po/`
  güncelleyin.
- **Yapı:** sistem etkileşimi sadece `managers/` altında; sayfalar ince kalsın.
- **Test:** yeni manager/fonksiyon için en az bir birim test; veri dosyası
  değiştiyse `test_data_files.py` zaten kapsar.
- **Stil:** siyah/otomatik format yok — mevcut kod stiline uyun; yeni dosya
  adları `snake_case` (eski CamelCase dosyalar tarihî).
- **Lisans:** GPL-3.0; katkı otomatik olarak aynı lisansla gelir.

## Commit & PR

- Açık layan commit mesajları (bkz. geçmiş: `Rename Pardus to ParsLinux...`).
- PR açıklamasında: ne, neden, nasıl test edildi. Ekran görüntüsü olan UI
  değişikliklerinde görsel ekleyin.
- CI kırmızıysa merge edilmez — önce testleri yeşillendirin.

## Sürüm ve Değişiklik Kaydı

Önemli değişikliklerde `CHANGELOG.md` "Yayınlanmamış" bölümüne girdi ekleyin.
Sürüm yükseltme adımları: `VERSION.md`.

## Yardım Alın

- Sorular için GitHub issue açın.
- Güvenlik açıkları için **public issue açmayın**, maintainer'e özel ulaşın.
