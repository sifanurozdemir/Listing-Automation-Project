# 🚀 Dynamic Listing & Form Automation System

Bu proje, karmaşık kategori hiyerarşileri ve dinamik form yapıları içeren e-ticaret platformları için geliştirilmiş, operasyonel verimlilik odaklı bir otomasyon çözümüdür.

---

## 🛠️ Teknik Mimari ve Yetkinlikler

* **Framework:** Python & Playwright (Async)
* **Protocol:** CDP (Chrome DevTools Protocol) entegrasyonu ile "Bypass MFA" stratejisi
* **Data Handling:** Pandas ile yapılandırılmamış veri setlerinin sistem hiyerarşisine uygun eşleştirilmesi (Mapping)

---

## 🚀 Kurulum ve Çalıştırma Rehberi

Sistemin stabil çalışması için aşağıdaki adımların sırasıyla takip edilmesi kritiktir.

---

### 1. Ortam Hazırlığı ve "Zombi" Süreç Temizliği

Sistemde oluşabilecek çakışmaları önlemek adına mevcut tarayıcı süreçlerini sonlandırın:

```bash
taskkill /F /IM chrome.exe /T
```

---

### 2. Tarayıcıyı Debug Modunda Başlatma

Projenin hedef platformdaki oturumu yönetebilmesi için Chrome'un belirtilen port üzerinden dinlenmesi gerekir:

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Proje_Yolunuz\chrome_profil"
```

**Not:** Açılan tarayıcı penceresi tüm otomasyon süreci boyunca aktif kalmalıdır.

---

### 3. Oturum Yönetimi (Session Persistence)

Hedef platformda manuel giriş yaptıktan sonra, oturum verilerini (cookies, storage) mühürlemek için :

```bash
python session_manager.py
```

Bu işlem sonunda `auth.json` dosyası oluşturulacaktır.

---

### 4. Otomasyonu Başlatma (The Listing Engine)

Tüm hazırlıklar tamamlandıktan sonra toplu veri girişini tetiklemek için:

```bash
python listing_engine.py
```

---

## ⚠️ Mühendislik Notları & Troubleshooting

* **Interrupt:** İşlemi durdurmak için terminalde `Ctrl + C` kombinasyonunu kullanın.

* **Session Reset:** "Oturum Hatası" alınması durumunda `auth.json` ve `chrome_profil` klasörlerini silerek 1. adımdan itibaren süreci tekrarlayın.

* **Rate Limiting:** Sistem, platform limitlerine takılmamak adına `slow_mo` ve asynchronous `sleep` fonksiyonları ile optimize edilmiştir.

---

## 👨‍💻 Geliştirici

**Şifanur Özdemir**
