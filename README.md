# SHEIN Web Scraping & Analiz Projesi


## Amaç

SHEIN, online web sitesi üzerinden satın alım imkanı sunan bir moda perakendecisidir. Ürünlerin adı, fiyatı, türü, satılan sanal marketi, indirim oranı ve müşteri inceleme sayısı gibi farklı bilgiler web sitede mevcut. Bu analizin amacı, belirtilen verilerin web site üzerinden kod aracılığıyla çekilip anlamlı sonuçlar için analiz edilmesine dayanıyor.

## Kullanılan Araçlar

Web siteden verilerin çekilmesi için Python programlama dili üzerinden Selenium kütüphanesi, yardımcı olması için NumPY ve Pandas gibi veri manipülasyon ve temizleme kütüphaneleri de kullanıldı. Xlsx formatında dışarı aktarılan veri, görselleştirme ve metrikslerin oluşturulması için PowerBI ortamına aktarıldı. Tüm grafikler ve metriksler PowerBI ortamında oluşturuldu.


## Veri Kazıma & Ön İşleme

[Veri Kaynağı](https://us.shein.com/recommend/Women-New-in-sc-100161222.html?adp=35242185&categoryJump=true&ici=us_tab03navbar03menu01dir02&src_identifier=fc%3DWomen%20Clothing%60sc%3DWomen%20Clothing%60tc%3DShop%20by%20category%60oc%3DNew%20in%60ps%3Dtab03navbar03menu01dir02%60jc%3DitemPicking_100161222&src_module=topcat&src_tab_page_id=page_home1718006855109)

Proje için sağlanan bağlantı sayfasındaki tüm ürünler, kazıma sürecinde kullanıldı. Kod 17 Haziran'da çalıştırıldığında 113 ürün web siteden çekildi. Web sitedeki elementler, Selenium driverı kullanılarak, class isimleriyle elemanların bulunmasıyla çekildi. Ek olarak, sleep fonksiyonları web sitedeki işlemlerin Captcha doğrulamasına yönlendirilmemesi için uzun tutuldu.

```Python
...
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


## Tools

- R Studio
  -  [Download here](https://posit.co/download/rstudio-desktop/#download)
 


## Data Preparation/Cleaning

In the initial data preparation phase, we performed the following tasks:
1. Loading the data and inspecting.
2. Handling NA values.
3. Data cleaning and formatting.



## Descriptive Data Analysis

It is important to establish the boundaries and stages of a dataset. To achieve this, we look into the data. Upon analyzing the data, we have discovered the following insights:

- In the NBA, there are five main player positions: Power Forward (PF), Center (C), Point Guard (PG), Shooting Guard (SG), and Short Forward (SF). According to the pie chart, the majority of players fall under the Shooting Guard position, while the least number of players are categorized as Centers. When creating a clustering model, the prediction will be based on the player's position.
![Position_Distribution](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/7ea5a8ab-7089-4b13-b353-f0d399657fee)

- The age range of NBA players is between 19 to 39 years old. On the other hand, there is no evidence to suggest that age affects the number of points scored in the NBA(13% correlation). Therefore, it is not possible to directly attribute a player's performance to their age.
![Data-Visualization_Age-Distribution](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/f430afe8-e447-4781-b5fd-916e545d0b33)

- Each player has played for a different length of time in the current season. We can see this in the 'MP' (minutes played) column, which ranges from 2 to 616. We assume that players who play less may have a lower chance of being selected as All-Stars. In addition, there is a strong correlation between the number of minutes played and points scored, with a correlation of 90%. This implies that a player's performance is directly related to the amount of time they spend on the court. Players who play for longer periods are more likely to be selected as All-Stars. To eliminate NBA player candidates with insufficient experience and game time, we removed players who have played less than 30% of the total minutes played by all players. We used the ` quantile()`  function to calculate the time range of all players.

```R
# Detect outlier
lower_bound <- quantile(nba_raw_data_v3$MP, 0.3)

outlier_row <- which(nba_raw_data_v3$MP > lower_bound)

nba_raw_data_v4 <- nba_raw_data_v3[outlier_row, ]
```
  
- The PTS column ranges from 0 to 488, indicating that some players have not scored any points this season. 
  
![Data-Visualization_PTS-Distribution](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/5e96eeb4-4790-42ce-b130-fc59fa4ec69b)

- In general, the NBA has a wide range of statistical data. This is due to the presence of unique players who have varying stats from one another.

## Predictive Analytics

As previously mentioned, we predicted the All-Star players based on their positions. We used the Elbow method and Hierarchical clustering to determine the appropriate number of clusters.

```R
# Elbow Method
fviz_nbclust(nba_players_center_v2.scaled, kmeans, method = "wss", k.max=12)
```
![Center_Elbow](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/12897004-2043-437e-9950-2833b5e5a7b6)

```R
# for Hierarchical Clustering (Ward's Clustering) 
set.seed(1234)
dist.res <- dist(nba_players_center_v2.scaled, method = "euclidean")
center_cust_Clustering <- hclust(dist.res, method = "ward.D")
plot(center_cust_Clustering, labels = FALSE, hang = -1) # Visualization of hclust
rect.hclust(center_cust_Clustering, h=20) # Visualization of hclust - draw rectangle
```
![Center_Hiearchial](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/87cfdb6d-60b8-4bdc-a114-18b7536b8220)

We used two methodologies to determine the correct number of clusters for each position. Once we had determined the number of clusters, we used the `cutree()` function to create the clusters. Finally, we checked the clusters on graphs that we created using the `ggplot2` package. Based on the graphs, we identified the clusters that represented the data points of the most successful players. Using this information, we were able to determine the most successful NBA players.

```R
# Assign clusters to origin of data points based on the cluster number
center_cust_cluster <- cutree(center_cust_Clustering, k=5) 
table(center_cust_cluster)

# Integrating segments into dataset
center_cust_clusters <- data.frame()
center_cust_clusters = data.frame(nba_players_center_v1, center_cust_cluster)
View(center_cust_clusters)

# View the segmentation graph
ggplot(center_cust_clusters, aes(x=PTS, y=TRB , color = factor(center_cust_clusters$center_cust_cluster))) + geom_point()

# list the predicted all-star players
View(center_cust_clusters[center_cust_clusters$center_cust_cluster==2, ])
```

![Clustering_ggplot2_visual](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/0d91143f-1ae3-4d9d-b619-974c51ac0575)

Cluster 2 shows the most successful NBA center players. We used the same methodology for every position. Please find the results of the clustering analysis below.

### Centers
![ClusteringResults_Allstar_Center](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/27bf8b33-bc39-41be-b793-3386dfe967ed)

### Point Guards
![ClusteringResults_Allstar_PointGuard](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/7a257fff-95d8-48d7-ba36-9d72fb7e223e)

### Power Forwards
![ClusteringResults_Allstar_PowerForward](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/8ba97cc2-831f-4546-9f97-da07ec368e93)

### Shooting Guards
![ClusteringResults_Allstar_ShootGuard](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/453a5456-ce76-463c-aaf1-78621aad52b1)

### Small Forwards
![ClusteringResults_Allstar_SmallForward](https://github.com/sonielyy/NBA-All-Stars-Prediction-Analysis/assets/71605453/fb3be30a-c097-491d-9e88-ffbd0b256021)


## Final Thoughts

We have carefully chosen the most skilled players and made predictions on who is likely to be selected as All-stars. The voting period will end on January 20, 2024. On January 25, TNT will announce the NBA All-stars, and we will compare our predictions with the actual All-stars.

Based on the first fan returns, our prediction model correctly predicted 68% of the top voted players and suggested 10 additional names for prediction.
[First Fan Returns](https://twitter.com/NBAPR/status/1742969199549358405)

## References

-	https://nbaexperiences.com/fr/blog/2024-nba-all-star-getting-around-guide
-	https://www.basketball-reference.com/leagues/NBA_2024_per_game.html







