# SHEIN Web Scraping & Analiz Projesi


## Amaç

SHEIN, online web sitesi üzerinden satın alım imkanı sunan bir moda perakendecisidir. Ürünlerin adı, fiyatı, türü, satılan sanal marketi, indirim oranı ve müşteri inceleme sayısı gibi farklı bilgiler web sitede mevcut. Bu analizin amacı, belirtilen verilerin web site üzerinden kod aracılığıyla çekilip anlamlı sonuçlar için analiz edilmesine dayanıyor.

![image](https://github.com/sonielyy/shein_scraping_project/assets/71605453/c5b20b8a-9fff-4339-ae55-154df7a765bc)


## Kullanılan Araçlar

Web siteden verilerin çekilmesi için Python programlama dili üzerinden Selenium kütüphanesi, yardımcı olması için NumPY ve Pandas gibi veri manipülasyon ve temizleme kütüphaneleri de kullanıldı. Xlsx formatında dışarı aktarılan veri, görselleştirme ve metrikslerin oluşturulması için PowerBI ortamına aktarıldı. Tüm grafikler ve metriksler PowerBI ortamında oluşturuldu.


## Veri Kazıma & Ön İşleme

[Veri Kaynağı](https://us.shein.com/recommend/Women-New-in-sc-100161222.html?adp=35242185&categoryJump=true&ici=us_tab03navbar03menu01dir02&src_identifier=fc%3DWomen%20Clothing%60sc%3DWomen%20Clothing%60tc%3DShop%20by%20category%60oc%3DNew%20in%60ps%3Dtab03navbar03menu01dir02%60jc%3DitemPicking_100161222&src_module=topcat&src_tab_page_id=page_home1718006855109)

Proje için sağlanan bağlantı sayfasındaki tüm ürünler, kazıma sürecinde kullanıldı. Kod 17 Haziran'da çalıştırıldığında 113 ürün web siteden çekildi. Web sitedeki elementler, Selenium driverı kullanılarak, class isimleriyle elemanların bulunmasıyla çekildi. Ek olarak, sleep fonksiyonları web sitedeki işlemlerin Captcha doğrulamasına yönlendirilmemesi için uzun tutuldu.

```Python
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
...
# Item Elements
name_elements = driver.find_elements(By.CLASS_NAME, 'product-card__goods-title-container')
sleep(2)

# Price Elements
price_elements = driver.find_elements(By.CLASS_NAME, 'product-card__prices-info')
sleep(2)
```
Veri çekildiğinde birçok noktalama işareti ve gereksiz karakterler mevcuttu. Bunlar tespit edilip temizlendi.

```Python
# Adjust the Price Col
def clean_data(data):
    data = data.replace('$', '').replace('%', '')
    amount_change = data.split('\n')
    amount = float(amount_change[0])
    change = int(amount_change[1]) if len(amount_change) > 1 else None
    return amount, change

df1[['Product_Price', 'Price_Discount_Rate']] = pd.DataFrame(df1['Price'].apply(clean_data).tolist(), index=df1.index)
...
```

'ProductName' sütununun içinde geçen kelimelere bakılarak, ürünün türüne ve market yerine ulaşmak için kodlar yazıldı.

```Python
...
# Define the product type by Keywords at Title
def product_identifier(text):
    if 'T-shirt' in text or 'T-Shirt' in text:
        return 'T-Shirt'
    elif 'Bikini' in text:
        return 'Bikini'
    elif 'Cardigan' in text:
        return 'Cardigan'
    elif 'Vest' in text:
        return 'Vest'
...
df1['Product_Type'] = df1['ProductName'].apply(product_identifier)
```

Ön işlemenin sonunda 7 sütun ve 113 satırdan oluşan temiz bir tablo oluşturuldu. Bu tablo xlsx formatında Python ortamından dışarı aktarıldı.

![image](https://github.com/sonielyy/shein_scraping_project/assets/71605453/0e0be087-22fb-45be-8ddd-b12378e15b25)

## Veri Analiz & Görselleştirme

### Ürünlerin Genel Durumu

![image](https://github.com/sonielyy/shein_scraping_project/assets/71605453/82fa5b82-bf0c-45a3-872b-6e3fc874026c)

113 ürün ilanını incelediğimizde:
- 15 farklı tipteki ürüne(T-shirt, şort, bikini,..) ve 20 farklı markete(SHEIN EZwear, SHEIN LUNE,..) ait bir ürün listesi elimizde.
- Ürünlerin fiyatı $3-$23 arasında değişkenlik gösteriyor, ortalama fiyat ise $8,2.
- Kaydedilen ürün incelemeleri web sitede '+100' veya '+1000' şeklindeki formatlarda tutulduğu için 'Minimum verilen oy' üzerinden analiz yapıldı. Ortalama oy değeri 438'e düşmekte.
- 'NEW' etiketiyle satılan ürünler, tüm ürün ilanlarının çoğunluğunu (%81,42) oluşturmakta.
- İndirim oranı ise %3 ile %20 arasında değişiklik gösteriyor. Ortalama ürün indirim oranı ise %8.

### Ürün Fiyatları

![image](https://github.com/sonielyy/shein_scraping_project/assets/71605453/8eb12862-9f6d-40e3-b6da-18ae251970d3)

Ortalama fiyatlar üzerinden ürün tipi ve markete göre yorum yapacak olursak:
- Hırka ($16,74) ve elbise ($14,89), satılan ürünler arasından en pahalı ürünler.
- Crop ($5,22) ve fanila ($5,87) ise satılan ürünler arasından en ucuz ürünler.
- SHEIN WYWH ($20,39) ve SHEIN JORESS ($18,19) en pahalı sanal marketler.
- SHEIN Qutie ($5,29) ve SHEIN Coolane ($5,69) ise en ucuz marketler.

### Ürün Adedi

![image](https://github.com/sonielyy/shein_scraping_project/assets/71605453/f4041afd-3dd1-47e0-bd41-cdf6fa67798a)

Farklı ürün sayısını ürünlerin tipine ve marketlerine göre yorumlarsak: 
- Üst kıyafetleri (24) ve T-shirtler (20) en fazla sayıda olanlar.
- Jean pantolonlardan, elbiseden ve bikiniden sadece birer tane bulunmakta.
- En ünlü market yerleri SHEIN LUNE (33) ve SHEIN EZwear (29).
- Birçok market yerinde birer tane ürün satılmakta.

### Ürün Değerlendirmesi

![image](https://github.com/sonielyy/shein_scraping_project/assets/71605453/a91b41f7-895a-44ee-9860-1649704dd6fe)

Ürün değerlendirmelerini incelediğimizde:
- Jeans pantolon ve üst-şort olarak satılan ürünlere ait ortalama +1000'den fazla inceleme geldiği görülüyor.
- Öte yandan elbise ve kadın geceliğine verilen oylar sadece +100'den fazla.
- Marketlere baktığımızda 4 market +1000'den fazla ortalama oylarıyla galip: MUSERA, SHEIN BAE, SHEIN WYWH ve SHEIN Frenchy.
- 7 market ise sadece +100'den fazla inceleme almış.

### Ürün İndirimleri  

![image](https://github.com/sonielyy/shein_scraping_project/assets/71605453/0ab21e1a-3b12-42f1-83f7-1aaba932fa7a)

Son olarak ortalama ürün indirimlerini incelediğimizde:
- Jeans pantolon (%20) ve normal pantolon (%16), en yüksek indirime sahip ürünler.
- Kadın geceliği ise (%3) en az indirime sahip ürün.
- En yüksek indirimleri yapan marketlerde SHEIN Essnce (%14) ve SHEIN Qutie (%13) var.
- En düşük indirimleri yapan marketler ise ortalama %7'den yüksek indirim yapıyor.


## Özet

Analizi tamamladığımızda, 117 SHEIN ürünü için şu çıkarımları yapabiliyoruz:

- Jeans, elbise, hırka ve pantolonlar ortalama fiyatı en yüksek ürünler oluyor. Bu ürünler marketlerde sayıca az bulunuyor. Öte taraftan, bu ürünlerin indirim oranları diğer ürünlere göre yüksek. Bu da ortalama yüksek fiyatlarını daha cazip yapmak için bir strateji olabilir.
- Üst giyim ürün türlerini incelediğimizde(T-shirt, vest, top,..) $10'ın üstünde bir fiyat bulmak zor. Üstelik, SHEIN üzerinde sayıca en fazla ürün bu gruba ait. Fazla satılmalarından dolayı indirim oranları da bu ürünler için az(incelediğimizde %10'dan fazla indirim pek yok). Ürün incelemeleri de ortalama +500'den fazla diyebiliriz.
- SHEIN LUNE iki yönüyle öne çıkan bir market: Satılan ürün sayısı bakımından en fazla satan ilk 3 market arasında ve diğer marketlere göre en ucuz ortalama fiyat bu markette.
- SHEIN Essnce ise ortalamaya baktığımızda en fazla indirim oranına sahip. Ek olarak, bu markette de 10'dan fazla ürün bulunuyor.
- SHEIN WYWH ise en fazla indirim ve yüksek incelemeye sahip bir market. Ürün sayısının az olması da bir gerçek.
- SHEIN Qutie ve SHEIN Coolane de en ucuz marketler, fakat gelen incelemelere baktığımızda +100 değerlerini görmemiz, bu marketlerden alım yaparken tekrar düşünülmesi gerektiğini belirtiyor.







