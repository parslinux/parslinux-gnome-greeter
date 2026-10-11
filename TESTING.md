# TESTING.md — Test Rehberi

## Hızlı Başlangıç

```bash
pip install pytest          # tek gerekli bağımlılık
python -m pytest            # tüm testler (şu an: 29 test)
python -m pytest -v         # isimleri gör
python -m pytest tests/test_settings_manager.py -k set  # filtre
```

Testler **GTK/gi kurulu olmadan da çalışır**: `tests/conftest.py`, eksik
`gi`/`pydbus` modüllerinin yerine sahte (stub) nesneler enjekte eder. Bu sayede
CI'da ve minimal geliştirme ortamında başlessız test mümkündür.

## Yapı

```
pytest.ini                    # testpaths=tests, pythonpath=src
tests/
  conftest.py                 # gi/pydbus stub'ları (GI_STUBBED)
  test_settings_manager.py    # SettingsManager birim testleri (FakeSettings)
  test_layout_manager.py      # LayoutManager mantığı + layout_config.json
  test_data_files.py          # JSON/UI/şema dosyalarının bütünlüğü
```

## Test Katmanları

1. **Veri bütünlüğü (parametrize):** `data/json/*.json` geçerli JSON, `data/ui/**/*.ui`
   geçerli XML, gschema doğru ID'yi kullanıyor. Yeni veri dosyası eklenince
   otomatik kapsanır.
2. **Birim testleri:** Manager saf mantığı, monkeypatch ile izole. Gerçek
   dconf/dbus'a **asla** dokunmazlar.
3. **(Eksik) Entegrasyon testi:** Gerçek GNOME oturumunda sayfa akışı — hâlâ
   manuel; isterseniz `dogtail`/AT-SPI ile ileride eklenebilir.

## Yeni Test Yazma Kuralları

- Modülü GTK'tan bağımsız yüklemeniz gerekiyorsa `test_settings_manager.py`'deki
  `importlib.util.spec_from_file_location` kalıbını kullanın.
- GSettings gerekiyorsa `FakeSettings` + `monkeypatch.setattr(modül, "GLib", ...)`
  deseni örnek alın.
- Test adı ne denediğini söylesin: `test_set_writes_back`, `test_set_unknown_key_does_not_raise`.
- CI'da `-p no:libtmux` zaten `pytest.ini`de tanımlıdır (bozuk harici eklenti
  çakışmasını önler).

## Çalıştırma Ortamları

| Ortam | Komut | Not |
|---|---|---|
| Lokal | `python -m pytest` | Python ≥ 3.10 yeterli |
| CI (GitHub Actions) | önerilen workflow aşağıda | gtk'suz koşar |
| Paket sonrası smoke | `parslinux-gnome-greeter --version` vb. | gerçek masaüstünde |

### Önerilen GitHub Actions snippet'i

```yaml
- name: Testler
  run: |
    pip install pytest
    python -m pytest
```

## Kapsam Dışı / Bilinen Sınırlar

- Sayfa sınıfları (pages/) GTK widget'larına bağlı olduğu için henüz unit test
  kapsamı dışında; stub'lar derin etkileşimi taklit etmez.
- Wallpapers indirme ağı gerektirir; mock HTTP ile ayrı test önerilir.
