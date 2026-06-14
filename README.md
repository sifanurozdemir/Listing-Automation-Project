<div align="left">
  <span style="font-size: 2.2em; font-weight: bold; vertical-align: middle; font-family: 'Outfit', 'Inter', sans-serif; color: #0284c7;">🤖 Dynamic Listing & Form Automation System</span>
</div>

---

<p align="left">
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://playwright.dev"><img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright"></a>
  <a href="https://pandas.pydata.org"><img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"></a>
  <a href="https://developer.chrome.com/docs/devtools"><img src="https://img.shields.io/badge/CDP_Protocol-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Chrome DevTools Protocol"></a>
  <a href="https://openpyxl.readthedocs.io"><img src="https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white" alt="Microsoft Excel"></a>
</p>

Bu proje, karmaşık kategori hiyerarşileri ve dinamik form yapıları içeren e-ticaret platformları için geliştirilmiş, operasyonel verimlilik odaklı bir otomasyon çözümüdür. 

Playwright tabanlı asenkron altyapısı ve **CDP (Chrome DevTools Protocol)** entegrasyonu sayesinde tarayıcı profili yönetebilir, oturum verilerini (Cookies & Storage) saklayabilir ve iki faktörlü doğrulamaları (MFA) manuel olarak aştıktan sonra kesintisiz ilan girişleri yapabilirsiniz.

---

## 📐 Teknik Mimari ve İş Akış Şeması

Sistemin çalışma prensibi, veri akışı ve oturum yönetimi adımları aşağıdaki mimari şemada gösterilmiştir:

```mermaid
graph TD
    %% Custom Styles for a modern look
    classDef source fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a;
    classDef script fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d;
    classDef output fill:#fff5f5,stroke:#ef4444,stroke-width:2px,color:#991b1b;
    classDef browser fill:#f0f9ff,stroke:#0ea5e9,stroke-width:2px,color:#075985;

    XLS[📄 ilanlar.xlsx<br/><b>İlan Veri Seti</b>]:::source -->|1. Veri Okuma| LE[⚙️ listing_engine.py<br/><b>Otomasyon Motoru</b>]:::script
    IMG[📂 resimler/<br/><b>Ürün Görselleri</b>]:::source -->|2. Eşleştirme & Yükleme| LE
    
    CH[🌐 Google Chrome<br/><b>Remote Debug (9222)</b>]:::browser <-->|3. CDP Protokolü| SM(🔑 session_manager.py<br/><b>Oturum Yönetici</b>):::script
    SM -->|4. Çerezleri Kaydet| AUTH[📄 auth.json<br/><b>Oturum Çerezleri</b>]:::output
    
    AUTH -->|5. Oturumu Yükle| LE
    LE <-->|6. Formları Doldur & Gönder| CH
```

---

## 📂 Proje Dizin Yapısı

Temiz kodlama standartlarına uygun olarak tasarlanmış dosya ve klasör ağacı:

```plaintext
📂 Listing-Automation-Project
├── 📂 chrome_profil          # Chrome kullanıcı profili verileri (Otomatik oluşturulur)
├── 📂 resimler               # İlanlara eklenecek ürün resimlerinin kategorize edildiği klasör
├── 📄 .gitignore             # Git dışı bırakılacak yerel profiller ve oturum dosyaları
├── 📄 auth.json              # Başarılı giriş sonrası oturum bilgilerini tutan mühür dosyası
├── 📄 ilanlar.xlsx           # İlan başlıkları, açıklamaları ve özellikleri içeren Excel tablosu
├── 📄 listing_engine.py      # Playwright tabanlı dinamik form doldurma ve ilan yükleme motoru
├── 📄 requirements.txt       # Projenin çalışması için gerekli Python kütüphaneleri
├── 📄 session_manager.py     # Hedef platformda bir kez oturum açıp auth.json üreten betik
└── 📄 README.md              # Proje kullanım kılavuzu ve teknik dokümantasyon
```

---

## 🚀 Kurulum ve Çalıştırma Rehberi

Sistemin stabil bir şekilde çalışabilmesi için aşağıdaki adımları sırasıyla uygulayın.

### 📋 Ön Gereksinimler

| Gereksinim | Kurulum / Detay | Amaç |
| :--- | :--- | :--- |
| **🐍 Python** | 3.10 veya üzeri bir sürümün yüklü olduğundan emin olun. | Betiklerin ve Playwright kütüphanesinin çalışması |
| **🌐 Google Chrome** | Sisteminize yerel olarak kurulu ve varsayılan yolda olmalıdır. | CDP protokolü üzerinden uzaktan kontrol |
| **📦 Python Kütüphaneleri** | `requirements.txt` dosyasındaki paketlerin yüklenmesi. | Pandas, Playwright ve Excel entegrasyonu |

---

### 1️⃣ Ortam Hazırlığı & Bağımlılıkların Yüklenmesi

1. Terminalde proje dizinine gidin ve bağımlılıkları yükleyin:
   ```powershell
   pip install -r requirements.txt
   ```
2. Playwright tarayıcı sürücülerini yükleyin:
   ```powershell
   playwright install
   ```

---

### 2️⃣ "Zombi" Süreç Temizliği

Sistemde oluşabilecek çakışmaları önlemek adına arka planda açık kalmış tüm Chrome süreçlerini sonlandırın:

```powershell
taskkill /F /IM chrome.exe /T
```

---

### 3️⃣ Tarayıcıyı Hata Ayıklama (Debug) Modunda Başlatma

Projenin hedef platformdaki oturumu yönetebilmesi için Chrome'u belirtilen port üzerinden dinlenecek şekilde başlatın:

```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\hp\Desktop\VS-Proje\Listing-Automation-Project\chrome_profil"
```

> [!IMPORTANT]
> - Açılan bu tarayıcı penceresi tüm otomasyon süreci boyunca **açık ve aktif** kalmalıdır.
> - `--user-data-dir` yolunun projenizin dosya yapısıyla eşleştiğinden emin olun.

---

### 4️⃣ Oturum Yönetimi (Session Persistence)

1. Açılan debug tarayıcısında hedef platforma gidin ve **manuel olarak giriş yapın (varsa MFA/SMS doğrulamalarını tamamlayın)**.
2. Giriş başarılı olduktan sonra yeni bir terminalden oturum verilerini mühürlemek için betiği çalıştırın:
   ```powershell
   python session_manager.py
   ```
   Bu işlem sonunda ana dizinde `auth.json` dosyası oluşturulacaktır.

---

### 5️⃣ Otomasyonu Başlatma (The Listing Engine)

Oturum kaydedildikten sonra Excel dosyasındaki ilanların sisteme yüklenmesini başlatın:

```powershell
python listing_engine.py
```

---

## ⚠️ Mühendislik Notları & Hata Giderme (Troubleshooting)

> [!NOTE]
> **İşlemi Durdurma:** Otomasyonu anlık olarak kesmek için terminal penceresinde `Ctrl + C` kombinasyonunu kullanabilirsiniz.

> [!TIP]
> **Oturumu Sıfırlamak (Session Reset):**
> 
> "Oturum Hatası" alıyorsanız veya oturumunuz sonlandıysa:
> 1. Ana dizindeki `auth.json` dosyasını ve `chrome_profil` klasörünü silin.
> 2. Chrome süreçlerini `taskkill` ile sonlandırıp 3. adımdan itibaren işlemleri tekrarlayın.

> [!IMPORTANT]
> **Limit Aşımı ve Hız Sınırları (Rate Limiting):**
> 
> Hedef platformların güvenlik/bot algılama sistemlerine takılmamak adına `listing_engine.py` içerisinde `slow_mo` parametreleri ve asenkron bekleme (`sleep`) süreleri optimize edilmiştir. Bu değerleri çok düşürmeniz hesabınızın geçici olarak engellenmesine yol açabilir.

---

## 👨‍💻 Geliştirici

**Şifanur Özdemir**
