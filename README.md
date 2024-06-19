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

113 ürün ilanını incelediğimizde; 
- 15 farklı tipteki ürüne(T-shirt, şort, bikini,..) ve 20 farklı markete(SHEIN EZwear, SHEIN LUNE,..) ait bir ürün listesi elimizde.
- Ürünlerin fiyatı $3-$23 arasında değişkenlik gösteriyor, ortalama fiyat ise $8,2.
- Kaydedilen ürün incelemeleri web sitede '+100' veya '+1000' şeklindeki formatlarda tutulduğu için 'Minimum verilen oy' üzerinden analiz yapıldı. Ortalama oy değeri 438'e düşmekte.
- 'NEW' etiketiyle satılan ürünler, tüm ürün ilanlarının çoğunluğunu (%81,42) oluşturmakta.
- İndirim oranı ise %3 ile %20 arasında değişiklik gösteriyor. Ortalama ürün indirim oranı ise %8.

### Ürün Fiyatları




## Final Thoughts

We have carefully chosen the most skilled players and made predictions on who is likely to be selected as All-stars. The voting period will end on January 20, 2024. On January 25, TNT will announce the NBA All-stars, and we will compare our predictions with the actual All-stars.

Based on the first fan returns, our prediction model correctly predicted 68% of the top voted players and suggested 10 additional names for prediction.
[First Fan Returns](https://twitter.com/NBAPR/status/1742969199549358405)







