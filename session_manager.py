import asyncio
from playwright.async_api import async_playwright

async def export_browser_context():
    """
    CDP (Chrome DevTools Protocol) üzerinden aktif bir tarayıcı oturumuna bağlanır 
    ve authentication state'i (cookies, storage vb.) persist etmek üzere dışa aktarır.
    """
    async with async_playwright() as p:
        # 9222 portunda 'remote-debugging-port' ile başlatılmış olan tarayıcıya bağlanıyoruz.
        # Bu yöntem, MFA (Multi-Factor Authentication) süreçlerini manuel aşmak için idealdir.
        try:
            endpoint_url = "http://localhost:9222"
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            print(f"Bağlantı Başarılı: {endpoint_url} üzerinden aktif oturuma erişildi.")
        except Exception as e:
            print(f"HATA: Aktif tarayıcı bulunamadı. Lütfen tarayıcıyı debug modunda başlattığınızdan emin olun. \nDetay: {e}")
            return

        # Mevcut tarayıcı instance'ı üzerinden aktif context ve sayfa yapısına erişim
        if not browser.contexts:
            print("HATA: Bağlanılan tarayıcıda aktif bir context bulunamadı.")
            return
            
        context = browser.contexts[0]
        
        print("\n--- Oturum Kayıt Süreci Başlatıldı ---")
        print("Lütfen hedef platformda oturum açtığınızdan ve ilgili sayfada olduğunuzdan emin olun.")
        
        input("\nKimlik doğrulama tamamlandıysa devam etmek için ENTER'a basın...")

        # Browser state (Cookies, Local Storage, Session Storage) JSON olarak serialize edilir.
        # Bu dosya, otomasyonun headless modda login bariyerine takılmadan çalışmasını sağlar.
        await context.storage_state(path="auth.json")
        print("\nBAŞARILI: Oturum verileri 'auth.json' dosyasına güvenli bir şekilde aktarıldı.")
        
        # Sadece CDP bağlantısı sonlandırılır, fiziksel tarayıcı penceresi açık kalmaya devam eder.
        await browser.close()

if __name__ == "__main__":
    asyncio.run(export_browser_context())