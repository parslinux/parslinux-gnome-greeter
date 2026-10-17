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
| [UYGULAMA_BAGLAMA.md](UYGULAMA_BAGLAMA.md) | Dağıtıma entegrasyon: autostart, şema, paket zinciri |
| `TERMS.md` / `SARTLAR.md` | Sistem gereksinimleri, lisans (GPL-3.0), dağıtım, marka ve garanti şartları |
| `TESTING.md` | Test çalıştırma, yazma kuralları, CI önerisi |
| `CONTRIBUTING.md` | Katkı kuralları, PR akışı |
| `CLAUDE.md` / `.claudeignore` | AI asistanları için bağlam ve hariç tutmalar |

### ✅ PEP 8 Taşınması & Geriye Dönük Uyumluluk
- `managers/` ve `components/` dosyaları PEP 8 `snake_case` isimlerine taşındı (`display_manager.py`, `layout_manager.py`, `about_dialog.py` vb.)
- Eski `CamelCase.py` modülleri geriye dönük uyumluluk katmanı (shim) olarak korundu
- Sabitler ve kaynak yolları merkezi `appinfo.py` modülüne taşındı
- Sayfa yapılandırması `page_registry.py` üzerinden lazy-loading mimarisine bağlandı

### ✅ Mimari & Performans İyileştirmeleri
- `main_window.py`: Tüm sayfaların doğrudan eager import edilmesi yerine `page_registry` üzerinden isteğe bağlı (on-demand / lazy) yüklenmesi sağlandı. Açılışta yalnızca aktif sayfa başlatılır.
- `pages/wallpaper.py`: Her görsel için kontrolsüz thread oluşturulması (thread storm) yerine `ThreadPoolExecutor(max_workers=4)` havuzu kuruldu. FlowBox içinde thumbnail sıralaması deterministik hale getirildi ve `os.system` çağrıları güvenli `subprocess.run` ile değiştirildi.
- `pages/layout.py`: `GifPaintable` animasyon döngüsüne `stop()` ve `cleanup()` eklendi; karttan çıkıldığında (`_on_card_leave`) zamanlayıcı iptal edilerek arka plandaki zombie timer ve CPU/bellek sızıntısı tamamen engellendi.
- `managers/extension_manager.py`: Eski harici `python-dbus` bağımlılığı kaldırılarak PyGObject'in yerleşik `Gio.DBusProxy` yapısına geçirildi; D-Bus bulunamadığında GSettings tabanlı zarif geri dönüş (fallback) eklendi.
- `managers/display_manager.py`: Monitör ayrıştırma döngüsü içindeki tekrarlı `dbus.SessionBus()` bağlantıları ve çağrıları elendi; `GetCurrentState` tek seferde çekilerek pydbus proxy'si üzerinden paylaştırıldı.
- `__main__.py`: Sabit kodlanmış `/usr/share/...` GResource yolu yerine; geliştirme dizini (`build/`), `XDG_DATA_DIRS`, `/usr/local` ve kullanıcı dizinlerini tarayan dinamik arama zinciri kuruldu.
- `pages/applications.py`: `parslinux-software`, `gnome-software`, `pamac-manager` ve `discover` mağazaları için dinamik geri dönüş ve bulunamadığında `Adw.AlertDialog` geri bildirimi eklendi.

### ✅ Hata Ayıklama & Kararlılık İyileştirmeleri
- `managers/settings.py`: Sistemde kurulu olmayan şemalara karşı `lookup()` koruması ve `set()` metoduna `list_keys()` anahtar doğrulaması eklendi; GLib `g_error()` kaynaklı `SIGABRT` çökmeleri önlendi.
- `pages/display.py`: DING (`org.gnome.shell.extensions.ding`) ve Nautilus şemaları `SettingsManager` üzerinden güvenli hale getirildi; kurulu olmayan sistemlerde çökmek yerine kontroller zarifçe gizlenir/devre dışı bırakılır.
- `managers/shortcut_manager.py`: `media-keys` ve `custom-keybinding` şemaları için varlık doğrulaması eklendi.
- `run.sh`: Dahili `--build` ve `--meson` bayraklarının Python uygulamasına parametre olarak sızması ve "Bilinmeyen seçenek" hatası vermesi engellendi.
- `pages/time.py`: `update_initial_state` içindeki girinti hatası (`return outside function` SyntaxError) düzeltildi
- `page_registry.py`: `import_module` bağıl import için `package=__package__` parametresi eklendi
- `pages/extension.py` & `pages/welcome.py`: Eksik gettext `_` importları tamamlandı
- `org.parslinux.parslinux-gnome-greeter.desktop.in`: msgfmt uyumu için standart anahtar isimleri (`Comment=`, `Keywords=`) kullanıldı
- `tests/conftest.py`: `GObject` desteği ve PEP 560 çoklu miras (`__mro_entries__`) desteği eklenerek tüm sayfa sınıflarının başlessız testi sağlandı
- Toplam test sayısı **37/37**'ye yükseldi ve tamamı başarıyla geçiyor.

## Devam Eden / Sonraki Adımlar

- ✅ Değişikliklerin düzenli bir **git commit** ile kaydedilmesi
- 🔜 GitHub Actions CI workflow (build + pytest)
- 🔜 ExtensionManager/WallpaperManager için mock tabanlı ek testler
- 🔜 Çeviri dosyalarında marka metinlerinin gözden geçirilmesi

## Bilinen Notlar

- Uygulama hâlâ "greeter" adıyla anılıyor ancak teknik olarak kurulum sonrası
  sihirbazdır (login ekranı değildir); isimlendirme ileride değişebilir.
- Flatpak manifesti yok (VERSION.md'de planlandı olarak işaretli).
