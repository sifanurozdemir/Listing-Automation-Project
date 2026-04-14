import pandas as pd
import asyncio
from playwright.async_api import async_playwright
import os

# --- KONFİGÜRASYON ---
# Platforma özel linkler ve sabitler genel değişkenlere atanmıştır.
BASE_URL = "https://www.target-marketplace.com/listing/new" 
CONTACT_INFO = "05XX XXX XX XX" # Kişisel veriler gizlendi
COMPANY_NAME = "Global Decorative Solutions"

# Kategori bazlı içerik üretim motoru (Template Engine)
CONTENT_TEMPLATES = {
    "tugla": {
        "title": "PREMIUM CLADDING BRICK | FACTORY DIRECT",
        "body": "Modern architectural solutions for interior and exterior projects. High durability and aesthetic design."
    },
    "tas": {
        "title": "DECORATIVE CULTURE STONE | ELEGANT SERIES",
        "body": "Natural textured wall cladding solutions. Lightweight and easy to install for various surfaces."
    },
    "barbeku": {
        "title": "PROFESSIONAL BBQ SYSTEM | SPECIAL EDITION",
        "body": "High-temperature resistant pumice material. Professional grilling experience for gardens and terraces."
    }
}

async def automated_listing_process():
    """
    Excel tabanlı veri setini okuyarak dinamik web formları üzerinden 
    otomatik ilan giriş süreçlerini yönetir.
    """
    # Veri kaynağının yüklenmesi
    df = pd.read_excel("listing_data.xlsx")

    async with async_playwright() as p:
        # 'slow_mo' ile anti-bot mekanizmalarına uyumlu insan simülasyonu hızı sağlanır.
        browser = await p.chromium.launch(headless=False, slow_mo=1200)
        
        # 'auth.json' üzerinden session persistence sağlanarak MFA/Login bariyerleri aşılır.
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        for index, row in df.iterrows():
            product_name = str(row['product_name'])
            category_type = str(row['category_type']).lower().strip()
            
            # --- Dinamik İçerik Oluşturma Mantığı ---
            template = CONTENT_TEMPLATES.get(category_type, {"title": row['ad_title'], "body": "Standard Listing"})
            final_content = f"{template['body']}\nContact: {CONTACT_INFO}\n{COMPANY_NAME}"

            print(f"\n>>> Processing [{index+1}/{len(df)}]: {product_name}")

            # 1. ADIM: MEDYA YÜKLEME SÜRECİ
            await page.goto(BASE_URL)
            
            # Mevcut taslak/uyarı kontrolleri (UX Flow Management)
            try:
                draft_button = page.get_by_role("button", name="Start New Listing")
                if await draft_button.is_visible(timeout=3000):
                    await draft_button.click()
                    await asyncio.sleep(2) 
            except:
                pass

            # Görsel dosyalarının sisteme dinamik olarak enjekte edilmesi
            img_folder = row['images_folder']
            images = [os.path.abspath(os.path.join(img_folder, f)) 
                      for f in os.listdir(img_folder) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            images.sort()

            async with page.expect_file_chooser() as fc_info:
                await page.get_by_text("Upload Images").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(images)
            
            # Asenkron yükleme süreci için tampon bekleme süresi
            await asyncio.sleep(25)
            await page.get_by_role("button", name="Continue").click()

            # 2. ADIM: FORM VERİLERİNİN ENJEKSİYONU
            await page.fill('input[name="ad_title_input"]', product_name)
            
            # Rich Text Editor (RTE) veya standart Textbox manipülasyonu
            desc_area = page.locator('div[name="Description"], #description-box')
            await desc_area.wait_for(state="visible")
            await desc_area.click()
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await desc_area.fill(final_content)

            # Dinamik Lokasyon Seçimi (Nested Dropdowns)
            for loc_val in [row['city'], row['district'], row['neighborhood']]:
                await page.get_by_text("Select Location").click()
                await page.keyboard.type(str(loc_val))
                await page.keyboard.press("Enter")
                await asyncio.sleep(1)

            await page.get_by_role("button", name="Next Step").click()

            # 3. ADIM: HİYERARŞİK KATEGORİ NAVİGASYONU
            # Excel'den gelen 'Kategori1 > Kategori2' yapısını parçalayarak dinamik seçim yapar.
            print("-> Navigating category hierarchy...")
            await asyncio.sleep(3) 

            try:
                category_path = str(row['category_path']).split('>')
                for segment in category_path:
                    # '.last' ve 'dispatch_event' kullanımı ile karmaşık DOM ağaçlarında 
                    # merkezleme ve tetikleme işlemleri yapılır.
                    target = page.get_by_text(segment.strip(), exact=True).last
                    await target.evaluate("el => { el.scrollIntoView({block: 'center'}); }")
                    await asyncio.sleep(1)
                    await target.dispatch_event("click")
                    await asyncio.sleep(2) 

                # Kategori onay butonu (id-based specific selector)
                await page.locator('#confirm_category_btn').click(force=True)

            except Exception as e:
                print(f"HATA: Kategori seçimi başarısız: {e}")
                input("Lütfen manuel seçim yapın ve ENTER'a basın...")

            # 4. ADIM: ÜRÜN ÖZNİTELİKLERİ (Conditional Rendering Handling)
            try:
                # 'Condition' ve 'Exchange' gibi conditional rendering içeren alanların yönetimi
                await page.locator('select[name="condition"]').select_option(label="New")
                await asyncio.sleep(2)

                # Takas seçeneği kontrolü
                swap_select = page.locator('select[name="exchange_option"]')
                if await swap_select.is_visible(timeout=5000):
                    await swap_select.select_option(label="No")

                await page.get_by_role("button", name="Continue").last.click(force=True)

            except Exception as e:
                print(f"HATA: Özellik seçiminde hata: {e}")

            # 5. ADIM: FİYATLANDIRMA VE FİNALİZASYON
            print(f"-> Setting price: {row['price']}")
            try:
                price_field = page.locator('#price_input_id')
                await price_field.fill(str(int(row['price'])))
                await asyncio.sleep(2)
                
                # İlanın yayına alınması (Final Confirmation)
                await page.get_by_role("button", name="Publish Listing").click(force=True)
                print(f"✅ SUCCESS: Listing '{product_name}' is live!")
                
            except Exception as e:
                print(f"HATA: Final aşamasında hata oluştu: {e}")

            # Rate-limiting ve IP blokajını önlemek için güvenli bekleme süresi
            print(f"Cooldown: Waiting 20 seconds for the next item...")
            await asyncio.sleep(20) 

        await browser.close()

if __name__ == "__main__":
    asyncio.run(automated_listing_process())