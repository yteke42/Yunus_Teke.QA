# Selenium Test Projesi - Insider Website

Bu proje Insider şirketinin websitesi için yazdığım Selenium testlerini içeriyor.  

## Proje Hakkında

Bu projede Insider websitesinin farklı sayfalarını test ettim.:
- Ana sayfa yüklenme testi
- Company menüsü ve Careers sayfası navigasyonu
- QA işleri filtreleme ve View Role butonuna tıklama

## Kullandığım Teknolojiler

- **Python 3.10** - Ana programlama dili
- **Selenium WebDriver** - Browser otomasyonu için
- **Chrome WebDriver** - Chrome browser'ı kontrol etmek için
- **unittest** - Test framework'ü
- **Page Object Model (POM)** - Kod organizasyonu için

## Dosyalar

Projede şu dosyalar var:
- `pages/` klasörü: Sayfa elementlerini tutuyorum
  - `base_page.py`: Temel sayfa sınıfı
  - `home_page.py`: Ana sayfa elementleri
  - `careers_page.py`: Kariyer sayfası elementleri
- `tests/` 
  - `base_test.py`: Temel test sınıfım
  - `tests.py`: Ana test dosyası
- `screenshots/`: Hata ekran görüntüleri

## Kurulum

1. **Python'u yükle** (3.10 veya üstü)
2. **Projeyi klonla** veya indir
3. **Gerekli kütüphaneleri yükle:**

```bash
pip install selenium
pip install webdriver-manager
```

## Testleri Çalıştırma

Proje klasörüne git ve şu komutları çalıştır:

```bash
cd Tester Selenium Project
```

```bash
py -3.10 -m tests.tests
```

## Test Açıklamaları

### 1. Ana Sayfa Testi (`test_homepage_is_opened`)
- Insider ana sayfasının yüklenip yüklenmediğini kontrol ettim.
- Sayfa başlığının doğru olup olmadığını kontrol ettim.
- URL'nin doğru olup olmadığını kontrol ettim.

### 2. Company Menüsü Testi (`test_company_menu_navigation_and_careers_blocks`)
- Company menüsüne tıklayıp Careers linkine gittim.
- Careers sayfasına yönlendirme olup olmadığını kontrol ettim.
- Sayfadaki blokların (Locations, Teams, Life at Insider) olup olmadığını kontrol ettim.

### 3. QA İşleri Testi (`test_qa_jobs_navigation_and_filtering`)
- QA careers sayfasına gittim.
- "See all QA jobs" butonuna tıkladım
- İşleri lokasyon (Istanbul, Turkiye) ile filtreledim.
- İşleri departman (Quality Assurance) ile filtreledim.
- View Role butonuna tıklayıp Lever sayfasına yönlendirme olup olmadığını kontrol ettim.

## Öğrendiğim Şeyler

### Page Object Model (POM)
- Her sayfa için ayrı sınıf yazdım
- Elementleri `__init__` metodunda tanımladım
- Kod tekrarını azalttım

### Explicit Wait
- `time.sleep()` yerine `WebDriverWait` kullandım
- Testler daha hızlı ve güvenilir oldu
- Farklı internet hızlarında çalışıyor

### XPath Locators
- Elementleri bulmak için XPath kullandım
- `contains()` fonksiyonu ile esnek arama yaptım
- Dinamik içerikler için uygun

### JavaScript Executor
- Normal click çalışmadığında JavaScript click kullandım
- `execute_script()` ile browser'da JavaScript çalıştırdım

## Karşılaştığım Sorunlar ve Çözümler

### 1. Element Click Intercepted
**Sorun:** Navbar elementler tıklamayı engelliyordu
**Çözüm:** JavaScript click kullandım

### 2. Location Dropdown
**Sorun:** Custom dropdown elementleri bulamıyordum
**Çözüm:** Explicit wait ile dropdown seçeneklerinin backend'den yüklenmesini bekledim

## Test Sonuçları

```
Ran 3 tests in 35.765s
OK
```

Tüm testler geçti.



