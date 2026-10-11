# SELF_HOSTING_GUIDE.md — Kendi Sunucunda Barındırma Rehberi

ParsLinux GNOME Greeter, çalışma sırasında dış kaynaklardan **duvar kağıdı**
ve benzeri içerikleri indirir (bkz. `data/json/wallpaper_sources.json`). Bu
belge, bu içerikleri kendi kontrol ettiğiniz bir sunucudan sunarak uygulamayı
tamamen bağımsız/kapalı ortamda çalıştırma yolunu anlatır.

## Neden Self-Hosting?

- Kurulum sonrası sihirbazı air-gapped (internetsiz) laboratuvar/sınıf ortamlarında çalıştırmak
- İndirme trafiğini yerel ağa çekerek bant genişliği ve gizlilik kontrolü
- ParsLinux markalı özelleştirilmiş içerik dağıtımı

## 1. Statik İçerik Sunucusu

En basit yöntem: dosyaları HTTP üzerinden sunan herhangi bir statik sunucu.

```bash
# Test amaçlı (Python)
python3 -m http.server 8080 --directory /srv/parslinux-assets

# Üretim: nginx örneği
server {
    listen 80;
    server_name assets.parslinux.local;
    root /srv/parslinux-assets;
    autoindex off;

    location ~* \.(png|jpg|webp)$ {
        expires 30d;
        add_header Cache-Control "public";
    }
}
```

> Not: Uygulama indirmeleri düz HTTP(S) GET ile yapar; ayrıca API gerekmez.
> TLS için Let's Encrypt veya iç CA sertifikası kullanın.

## 2. Kaynak Listesini Özelleştirme

`data/json/wallpaper_sources.json` içindeki URL'leri kendi sunucunuzla değiştirin:

```json
{
  "sources": [
    {
      "name": "ParsLinux Aurora",
      "url": "https://assets.parslinux.local/wallpapers/aurora.jpg"
    }
  ]
}
```

Değişiklikler paketle dağıtılabileceği gibi, geliştirme ortamında doğrudan
kaynaktan çalıştırıldığında (`meson compile` + yerel run) anında etkili olur.

## 3. Eklenti/İçerik Aynalama

Harici eklenti depolarını (extensions.gnome.org vb.) aynalamak isterseniz:

1. Gerekli eklenti `.shell-extension.zip` dosyalarını indirip
   `/srv/parslinux-assets/extensions/` altına koyun.
2. `data/json/extensions.json` içindeki UUID/versiyon alanlarını koruyarak
   indirme adreslerini güncelleyin.
3. GNOME'un kendi eklenti kurulumu shell sürümüne bağlıdır; kapalı ortamlarda
   ZIP'i kullanıcıya açıp `~/.local/share/gnome-shell/extensions/<uuid>/`
   altına kurma seçeneğini sayfa akışına eklemeniz gerekebilir.

## 4. Doğrulama

```bash
# URL'lerin erişilebilirliği
curl -sI https://assets.parslinux.local/wallpapers/aurora.jpg | head -1

# JSON şema geçerliliği (test altyapısı denetler)
python -m pytest tests/test_data_files.py -v
```

## 5. DNS / Yerel Çözümleme

Kapalı ağlarda `assets.parslinux.local` için lokal DNS ya da `/etc/hosts`
girdisi kullanın:

```
10.0.0.5   assets.parslinux.local
```

## Güvenlik Notları

- İndirilen içerik yalnızca statik medya olmalı; çalıştırılabilir betik sunmayın.
- HTTPS'i tercih edin; sertifika doğrulamasını kapatmayın.
- Sunucu loglarında IP tutulmasını en aza indirmek için access log'u kısıtlayın.
