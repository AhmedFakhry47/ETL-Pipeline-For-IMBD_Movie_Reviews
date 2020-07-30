# IMBD Reviews ETL Pipe line
A mongoDB stores thousands of reviews for over than 250 movies and all the information related to these movies. 

</b> 
In this repo, I implemented an ETL pipeline that to achieve the following:
1-Collect reviews and stars from the database. 
2-Filter the text and do the preprocessing task from: -Text Normalization-Noise Filteration-Stemming- 
3-Store the data in Json files or Csv files. 
</b>
</b>
Before that, There is an implementation of IMBD spider to crawl reviews from the website for 250 different movies from different genres. </b>
The crawled reviews are stored in mongoDB.
</b>

# Dependencies are: 
</b>
1-Scrapy
2-Pandas
3-shutil
4-re
5-Pymongo
6-Json
7-NLTK
</b>

# Screenshots 
# Data After Filteration
![All IN](https://github.com/AhmedFakhry47/ETL-Pipeline-For-IMBD_Movie_Reviews/blob/master/DataAfterFilteration.png)

# Reviews After Filteration
![Reviews](https://github.com/AhmedFakhry47/ETL-Pipeline-For-IMBD_Movie_Reviews/blob/master/Reviews.png)

# Database
![WordCloud](https://github.com/AhmedFakhry47/ETL-Pipeline-For-IMBD_Movie_Reviews/blob/master/Reviews_cloud.png)
