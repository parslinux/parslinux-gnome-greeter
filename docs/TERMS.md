# ParsLinux GNOME Greeter — Şartlar ve Koşullar (Terms & Conditions)

Bu belge, **ParsLinux GNOME Greeter** (kurulum sonrası yapılandırma sihirbazı)
uygulamasının hem **teknik/sistem çalışma şartlarını (gereksinimler)** hem de
**hukuki, lisans, dağıtım ve kullanım şartlarını** ayrıntılı olarak açıklamaktadır.

---

## 1. Sistem ve Donanım Şartları (Teknik Gereksinimler)

ParsLinux GNOME Greeter'ın kararlı, akıcı ve beklenen biçimde çalışabilmesi için
aşağıdaki donanım ve yazılım şartlarının karşılanması gerekir:

### 1.1. Donanım Şartları

| Bileşen | Minimum Şart | Önerilen Şart |
|---|---|---|
| **İşlemci (CPU)** | 64-bit x86 (x86_64) veya 64-bit ARM (aarch64) | 4 çekirdekli modern 64-bit işlemci |
| **Bellek (RAM)** | 2 GB RAM | 4 GB veya daha fazla RAM |
| **Ekran Çözünürlüğü** | 1024 × 768 piksel | 1920 × 1080 (Full HD) veya üzeri |
| **Disk Alanı** | ~50 MB (uygulama ve bağımlılıklar için) | 1 GB (indirilebilir duvar kağıtları için) |
| **Grafik Kartı** | OpenGL 3.2+ / Vulkan uyumlu GPU veya yazılımsal render (llvmpipe) | Donanımsal hızlandırma destekli GPU |

### 1.2. İşletim Sistemi ve Masaüstü Şartları

- **Hedef Dağıtım:** ParsLinux (birincil hedef) veya GNOME tabanlı herhangi bir modern Linux dağıtımı (Arch Linux, Debian 12+, Fedora 38+, Ubuntu 22.04+).
- **Masaüstü Ortamı:** GNOME Shell **>= 40.0** (tercihen GNOME 44 - 46+).
- **Görüntü Sunucusu:** Hem **Wayland** hem de **X11 (Xorg)** oturumları desteklenir.
- **Yetki Düzeyi:** Uygulama normal kullanıcı yetkileriyle (`non-root`) çalışmalıdır. Sistem ayarlarını değiştirmek için `sudo` gerektirmez; kullanıcı düzeyindeki GSettings/dconf veritabanını kullanır.

### 1.3. Yazılım ve Kütüphane Bağımlılıkları (Çalışma Zamanı)

| Yazılım / Kütüphane | Gerekli Sürüm | Açıklama |
|---|---|---|
| **Python** | `>= 3.8` (Önerilen: 3.10+) | Uygulamanın çekirdek çalışma zamanı |
| **PyGObject (`python3-gi`)** | `>= 3.42` | Python GObject Introspection köprüsü |
| **GTK 4 (`gir1.2-gtk-4.0`)** | `>= 4.10` | Modern arayüz bileşenleri |
| **Libadwaita (`gir1.2-adw-1`)** | `>= 1.2` | GNOME HIG tasarım sistemi ve widget'ları |
| **GLib / GIO / GSettings** | `>= 2.74` | Veri yapılandırması ve şema yönetimi |
| **python3-pydbus** | `>= 0.6` | Sistem ve oturum D-Bus entegrasyonu |
| **dconf** | `>= 0.40` | Kullanıcı tercihleri arka ucu |

### 1.4. Derleme ve Paketleme Şartları (Geliştirici / Dağıtımcı)

- **Meson:** `>= 0.60.0`
- **Ninja:** `>= 1.10`
- **GResource Araçları:** `glib-compile-resources`
- **GSettings Araçları:** `glib-compile-schemas`
- **Yerelleştirme:** `gettext` (`xgettext`, `msgfmt`, `msgmerge`)

---

## 2. Kullanım ve Lisans Şartları (Terms of Use)

ParsLinux GNOME Greeter, **GNU Genel Kamu Lisansı Sürüm 3 (GPL-3.0)** (veya kütüphane bileşenleri için LGPL-3.0) ile lisanslanmış bir **Özgür Yazılımdır**.

### 2.1. Tanınan Temel Haklar

Kullanıcılar ve kurumlar aşağıdaki haklara koşulsuz olarak sahiptir:

1. **Çalıştırma Özgürlüğü:** Yazılımı ticari, kurumsal, eğitim, kişisel veya kamu dahil herhangi bir amaçla kısıtlama olmaksızın çalıştırma hakkı.
2. **İnceleme ve Öğrenme Özgürlüğü:** Yazılımın kaynak kodunu inceleme, nasıl çalıştığını anlama ve kendi gereksinimlerine göre uyarlama hakkı.
3. **Kopyalama ve Paylaşma Özgürlüğü:** Yazılımın orijinal kopyalarını başkalarıyla ücretsiz veya ücretli olarak paylaşma hakkı.
4. **Geliştirme ve Dağıtma Özgürlüğü:** Yazılım üzerinde değişiklik yapma, hata düzeltme veya yeni özellik ekleme ve bu değiştirilmiş sürümleri kamuoyuna dağıtma hakkı.

### 2.2. Copyleft ve Karşılıklılık Şartı

GPL-3.0 lisansının getirdiği temel yükümlülükler şunlardır:

- **Kaynak Kod Erişimi:** ParsLinux GNOME Greeter'ı veya değiştirilmiş bir sürümünü ikili (binary/paket) biçimde dağıtan herkes, kaynak kodunu da aynı koşullarla kamuya açık biçimde sağlamakla yükümlüdür.
- **Aynı Lisansla Devam:** Yapılan geliştirmeler ve türev çalışmalar kapalı kaynaklı hale getirilemez; dağıtıldığında GPL-3.0 ile lisanslanmalıdır.
- **Telif Hakları ve Bildirimler:** Orijinal telif hakkı ve lisans bildirimleri kaynak dosyalardan silinemez veya değiştirilemez.

---

## 3. Dağıtım, Entegrasyon ve Yeniden Markalama Şartları

ParsLinux GNOME Greeter, bir Linux dağıtımına (özellikle ParsLinux'a) dahil edilirken
aşağıdaki şartlara uyulmalıdır:

### 3.1. Entegrasyon Kuralları

- **Otomatik Başlatma (Autostart):** Greeter, ilk oturum açılışında `/etc/xdg/autostart/org.parslinux.parslinux-gnome-greeter-autostart.desktop` dosyası üzerinden tetiklenir.
- **Kullanıcı İradesine Saygı:** Kullanıcı sihirbazı tamamladığında veya "Bir daha gösterme" seçeneğini işaretlediğinde, bu tercih dconf üzerinde saklanmalı ve kullanıcı zorla tekrar sihirbaza yönlendirilmemelidir.
- **Sistem Dosyalarını Bozmama:** Greeter yalnızca GNOME standart GSettings şemalarına (`org.gnome.desktop.*`) yazar; doğrudan sistem yapılandırma dosyalarını (`/etc/`) izinsiz ezmez.

### 3.2. Yeniden Markalama (Rebranding) ve Fork Şartları

- ParsLinux dışındaki bağımsız bir dağıtım bu sihirbazı kullanmak isterse:
  1. Gerekli logo, tema ve metin özelleştirmelerini yapabilir.
  2. Ancak resmi "ParsLinux" ismini ve logolarını sanki resmi bir ParsLinux ürünüymüş hissi verecek şekilde yanıltıcı kullanamaz.
  3. Kaynak kodunda geçmişe yönelik marka temizliği korunmalı; proje adlandırmasında eski veya ilgisiz isimler (örn. "Pardus") kullanılmamalıdır.

---

## 4. Marka, İsim ve Telif Hakları Şartları

- **"ParsLinux" Markası:** "ParsLinux" adı, logoları ve marka varlıkları ParsLinux projesine aittir.
- **Marka Ayrımı:** GPL-3.0 yazılım lisansı, kaynak kodu kopyalama hakkı verir ancak projenin tescilli markalarının izinsiz ve aldatıcı biçimde ticari kullanımını kapsamaz.
- **Türev Ürünler:** Projeyi fork eden veya türev ürün oluşturan geliştiricilerin kendi marka ve logolarını kullanmaları rica olunur.

---

## 5. Gizlilik, Güvenlik ve Telemetri Şartları

ParsLinux kullanıcı gizliliğine mutlak saygı gösterir:

- **Sıfır Telemetri:** ParsLinux GNOME Greeter; hiçbir analitik veri, donanım kimliği, kullanıcı bilgisi, IP adresi veya kullanım istatistiği toplamaz ve hiçbir harici sunucuya iletmez.
- **Yerel Veri Saklama:** Yapılan tüm kişiselleştirme seçimleri yerel dconf veritabanında (`org.parslinux.parslinux-gnome-greeter` ve GNOME şemalarında) tamamen cihaz üzerinde tutulur.
- **Ağ İletişimi:** Uygulama temel işlevleri için internet bağlantısına ihtiyaç duymaz (çevrimdışı çalışır). İsteğe bağlı duvar kağıdı indirme özellikleri haricinde hiçbir ağ çağrısı yapılmaz.

---

## 6. Kurumsal ve Ticari Kullanım Şartları

- **Ücretsiz Kullanım:** Şirketler, kamu kurumları ve eğitim kuruluşları ParsLinux GNOME Greeter'ı herhangi bir lisans ücreti ödemeden istedikleri sayıda iş istasyonunda kurabilir ve kullanabilir.
- **Ticari Hizmetler:** GPL-3.0 uyarınca, yazılımın kendisi için yapay lisans kısıtlamaları getirilemez; ancak özelleştirme, dağıtım hazırlama, entegrasyon ve teknik destek hizmetleri ticari olarak sunulabilir (ayrıntılar için: [PAYMENT_INTEGRATION.md](PAYMENT_INTEGRATION.md)).
- **Uygulama İçi Ödeme Kısıtlaması:** Standart Greeter akışında zorunlu ödeme veya lisans kilidi bulunamaz; bağış veya destek yönlendirmeleri yalnızca isteğe bağlı olarak "Kapanış (Outro)" veya "Hakkında" pencerelerinde yer alabilir.

---

## 7. Katkı ve Topluluk Şartları

ParsLinux GNOME Greeter'a katkıda bulunmak isteyen geliştiriciler ve tasarımcılar:

1. [CONTRIBUTING.md](CONTRIBUTING.md) rehberinde belirtilen kodlama ve PR standartlarına uymalıdır.
2. Gönderilen tüm kodların GPL-3.0 lisansı altında kamuya açık hale geleceğini kabul eder.
3. Test suite'ini (`pytest`) başarıyla geçen, ParsLinux marka kurallarına uygun ve yerelleştirilebilir (`_()`) kod sunmalıdır.

---

## 8. Garanti Reddi ve Sorumluluk Sınırları (Disclaimer of Warranty)

*(GPL-3.0 Madde 15 ve 16 uyarınca yasal bildirim)*

> **GARANTİ YOKTUR (AS IS):**  
> YÜRÜRLÜKTEKİ KANUNLARIN İZİN VERDİĞİ ÖLÇÜDE, BU PROGRAM İÇİN HERHANGİ BİR GARANTİ VERİLMEZ. TELİF HAKKI SAHİPLERİ VE/VEYA DİĞER TARAFLAR PROGRAMI, AÇIK YA DA ZIMNİ HİÇBİR GARANTİ OLMAKSIZIN "OLDUĞU GİBİ" SAĞLAR. PROGRAMIN KALİTESİ VE PERFORMANSINA İLİŞKİN TÜM RİSK SİZE AİTTİR. PROGRAMIN KUSURLU OLDUĞU ANLAŞILIRSA, GEREKLİ TÜM SERVİS, ONARIM VEYA DÜZELTME MASRAFLARI TARAFINIZA AİTTİR.

> **SORUMLULUK SINIRLAMASI:**  
> KANUNİ BİR ZORUNLULUK OLMADIKÇA VEYA YAZILI OLARAK ANLAŞILMADIKÇA, HİÇBİR TELİF HAKKI SAHİBİ YA DA PROGRAMI DEĞİŞTİREN/DAĞITAN HERHANGİ BİR TARAF; PROGRAMIN KULLANILMASI VEYA KULLANILAMAMASINDAN KAYNAKLANAN HERHANGİ BİR GENEL, ÖZEL, ARIZİ VEYA BAĞLI ZARARDAN (VERİ KAYBI, VERİNİN BOZULMASI YA DA SİZİN VEYA ÜÇÜNCÜ ŞAHISLARIN UĞRAYACAĞI ZARARLAR DAHİL) SORUMLU TUTULAMAZ.

---

## 9. İlgili Dokümantasyon

| Konu | İlgili Belge |
|---|---|
| Kurulum Adımları ve Paket Bağımlılıkları | [INSTALL.md](INSTALL.md) |
| Mimari Tasarım ve Katmanlar | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Katkı Sağlama Rehberi | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Veri Depolama ve GSettings Rehberi | [DATA_SAVING_GUIDE.md](DATA_SAVING_GUIDE.md) |
| Dağıtıma Bağlama ve Entegrasyon | [UYGULAMA_BAGLAMA.md](UYGULAMA_BAGLAMA.md) |
| Tam Lisans Metni | [LICENSE](../LICENSE) |
