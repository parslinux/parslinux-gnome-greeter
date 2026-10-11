# PAYMENT_INTEGRATION.md — Ödeme/Bağış Entegrasyon Rehberi

ParsLinux GNOME Greeter ücretsiz ve GPL-3.0 lisanslı bir uygulamadır; **içinde
zorunlu ödeme akışı bulunmaz.** Bu belge, projeyi finanse etmek isteyen
kurumların/geliştiricilerin uygulamanın UI akışını bozmadan **bağış veya
abonelik yönlendirmesi** eklemesi gereken yeri ve kuralları açıklar.

## Nereye Eklenmeli?

Uygun tek yer **outro (kapanış) sayfası** veya **Hakkında diyaloğu**dur:

- `src/parslinux_gnome_greeter/pages/outro.py` — sihirbaz tamamlanınca görünen sayfa
- `src/parslinux_gnome_greeter/components/AboutDialog.py` — "Bağış yap" butonu

Ödeme asla diğer sihirbaz sayfalarına (tema, duvar kağıdı, eklenti...) gömülmemeli;
kullanıcı yapılandırması ücretli hissettirilmemeli.

## Yöntem 1: Harici Bağış Sayfasına Yönlendirme (Önerilen)

En az temas, en güvenli yaklaşım — tarayıcıda ödeme sayfası açılır:

```python
from gi.repository import Gtk

def on_donate_clicked(self, button):
    Gtk.show_uri_on_window(
        self.get_root(),
        "https://parslinux.org/bagis",
        Gdk.CURRENT_TIME,
    )
```

`.ui` dosyasına `Adw.ActionRow` veya `Gtk.Button` ekleyip sinyalini bağlayın.

## Yöntem 2: Kripto Cüzdan / QR Kod

Outro sayfasına sabit bir QR görseli (`data/assets/donate_qr.png`) ve cüzdan
adresini kopyalama butonu ekleyin. Herhangi bir SDK gerekmez, çevrimdışı da çalışır.

## Yöntem 3: Sanal POS / Abonelik API'si (Kurumsal Sürüm İçin)

ParsLinux türevli **kurumsal/özel işaretli** bir derleme satılacaksa:

1. Lisans anahtarı doğrulama servisi kendinize ait bir backend'de tutulur
   (bkz. `SELF_HOSTING_GUIDE.md`).
2. Uygulamada sadece *hafif bir doğrulama çağrısı* yapılır:
   `POST /license/activate {key}` → `{ok, features}`.
3. Özellik bayrakları GSettings'e yazılır (`app_settings.set("pro-features", ...)`);
   topluluk derlemesinde bu bayrak hep `true` kalacak şekilde ayrıştırılmalıdır
   (GPL uyumu için kaynak kodundaki tüm özellikler açık olmalı, ödeme yalnızca
   *hizmet* karşılığı olmalıdır).
4. Kart bilgisi uygulama üzerinden **asla** geçmemeli — daima PCI-DSS uyumlu
   sağlayıcının barındırılan formu (Stripe Checkout, iyzico iframe vb.) kullanılmalı.

## Hukuki / Etik Kurallar

- GPL-3.0: ödeme, kullanıcının kaynak kod üzerindeki hakkını kısıtlayamaz. Satılabilen şey hizmet,
  destek veya özel markalı dağıtımdır.
- KVKK/GDPR: kişisel veri toplayan hiçbir ekran "varsayılan seçim" ile ilerlemez.
- Tüm ödeme bağlantıları çevrilebilir metinlerle (`_()`) sunulmalı ve
  `data/po/*.po` dosyalarında yer almalıdır.

## Test

Bağış butonu eklediyseniz:
- `tests/test_data_files.py` yeni `.ui` dosyasını otomatik doğrular.
- Buton sinyali için GTK olmadan çalışan birim testi: callback'in ürettiği URI'yi
  sahte `show_uri` ile assert edin.
