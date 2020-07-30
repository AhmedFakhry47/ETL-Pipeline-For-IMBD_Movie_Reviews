# IMBD Reviews ETL Pipe line
A mongoDB stores thousands of reviews for over than 250 movies and all the information related to these movies.\


<p>In this repo, I implemented an ETL pipeline to achieve the following:</p>
<ul>
<li> Collect reviews and stars from the database.</li>
<li> Filter the text and do the preprocessing task from: -Text Normalization-Noise Filteration-Stemming-.</li>
<li> Store the data in Json files or Csv files.</li>
</ul>

Before that, There is an implementation of IMBD spider to crawl reviews from the website for 250 different movies from different genres.\
The crawled reviews are stored in mongoDB.

# Dependencies are: 
<ul>
<li>Scrapy</li>
<li>Pandas</li>
<li>shutil</li>
<li>re</li>
<li>Pymongo</li>
<li>Json</li>
<li>NLTK</li>
</ul>

# Screenshots 
# Data After Filteration
![All IN](https://github.com/AhmedFakhry47/ETL-Pipeline-For-IMBD_Movie_Reviews/blob/master/DataAfterFilteration.png)

# Reviews After Filteration
![Reviews](https://github.com/AhmedFakhry47/ETL-Pipeline-For-IMBD_Movie_Reviews/blob/master/Reviews.png)

# Database
![WordCloud](https://github.com/AhmedFakhry47/ETL-Pipeline-For-IMBD_Movie_Reviews/blob/master/Reviews_cloud.png)
