<h1><b><font color="#cc0000"><i>Clustering customers </i></font></b></h1>





<h1>1- Overview and business problem</h1>

<br>
<p><font size="3">A UK-based online retail store has captured the sales data for different products for the period of one year (Nov 2016 to Dec 2017). The organization sells gifts primarily on the online platform.</br> The customers who make a purchase consume directly for themselves. There are small businesses that buy in bulk and sell to other customers through the retail outlet channel.</font></p>

<p><font size="3">The organization wants to roll out a loyalty program to the high-value customers after identification of segments, therefore it is important to find significant customers for the business who make high purchases of their favourite products. A common approach to rank valuable customers is the <a href="https://www.techtarget.com/searchdatamanagement/definition/RFM-analysis#:~:text=What%20is%20RFM%20(recency%2C%20frequency%2C%20monetary)%20analysis%3F,and%20perform%20targeted%20marketing%20campaigns.">RFM analysis</a> technique, however this approach can not be seen as silver bullet, so there are many cases where this technique is not the best approach. Therefore, machine learning clustering methodologies were implemented aimed to segment customers into different groups with focus on the most valuable customers (we are going to call them 'Golden' customers). The final succeded model was further sucessifully applied providing a table that can be consulted via SQL query and consumed by any data visualization tool (Metabase, Power BI, Tableau, etc). The table contains mainly the identification code as well as the cluster where each customer belongs to.</font></p>

<p><font size="3"><b>Disclaimer:</b> The business context herein presented is fictitious and was used only for the purpose of the development of this project.</font></p>


<p><font size="3">Datasets used in this project can be downloaded <a href="https://www.kaggle.com/vik2012kvs/high-value-customers-identification">here</a>.</font></p>








<h1>2- Data description</h1>

<br>
  <font size="3">The dataset used to build the solution has the following attributes:</font></li>
<br>
<br>
<ul>
  <li><font size="3"><b>Invoice Number - </b>Invoice number (A 6-digit integral number uniquely assigned to each transaction)</font></li><br>
  <li><font size="3"><b>StockCode - </b>Product (item) code</font></li><br>
  <li><font size="3"><b>Description - </b>Product (item) name</font></li><br>
  <li><font size="3"><b>Quantity - </b>The quantities of each product (item) per transaction</font></li><br>
  <li><font size="3"><b>InvoiceDate - </b>The day when each transaction was generated</font></li><br>
  <li><font size="3"><b>UnitPrice - </b>Unit price (Product price per unit)</font></li><br>
  <li><font size="3"><b>CustomerID - </b>Customer number (Unique ID assigned to each customer)</font></li><br>
  <li><font size="3"><b>Country - </b>Country name (The name of the country where each customer resides)</font></li><br>
</ul>








<h1>3- Solution strategy</h1>

<br>
<ol>
  <li><font size="3"><b>Understanding the business and problems to be solved:</b> search for the real reasons for the need for customers segmentation and how the problem can be solved through machine learning, which aspects should be considered and how better the proposal can be considering the solution currently being used in the company.</font></li>
<br>
  <li><font size="3"><b>Data colection:</b> downloading the corresponding .csv files from <a href="https://www.kaggle.com/vik2012kvs/high-value-customers-identification">Kaggle</a> plattform.</font></li>
<br>
  <li><font size="3"><b>Data cleaning:</b> basic search for missing values, outliers and inconsistencies to make data suitable for further analysis. Adittionally a basic inspection including descriptive statistics (mean, standard deviation, range, skewness and kurtosis) should be also carried out.</font></li>
<br>
  <li><font size="3"><b>Feature engineering:</b> creating new features from the existing ones to assist in both exploratory data analysis (EDA) and machine learning modelling.</font></li>
<br>
  <li><font size="3"><b>Data filtering and selection:</b>  reducing the data based on business assumptions and constraints to make training set as close as possible to data in production.</font></li>
<br>
  <li><font size="3"><b>EDA:</b> exploring data to search for interesting insights and understand the behavior of the features.</font></li>
<br>
  <li><font size="3"><b>Data preparation:</b> applying scaling, encoding and transformation methods to make data suitable to machine learning.</font></li>
<br>
  <li><font size="3"><b>Feature selection:</b> selecting the most relevant attributes based on EDA results to maximize machine learning performance.</font></li>
<br>
  <li><font size="3"><b>Hiperparameter fine tuning:</b> optimizing the parameter k for clustering algorithms, in other words, identify the right number of customer segments.If the number of observations is loaded in one of the clusters, breaking down that cluster further using the clustering algorithm. Here loaded means if any cluster has more number of data points as compared to other clusters then spliting that clusters by increasing the number of clusters and observe, comparing the results with previous results.</font></li>
<br>
  <li><font size="3"><b>Machine learning:</b> identifying the clustering algorithm that gives maximum accuracy and explains robust clusters.</font></li>
<br>
  <li><font size="3"><b>Cluster analysis:</b> describe the main aspects of Golden customers cluster.</font></li>
<br>
  <li><font size="3"><b>Deployment:</b> although solution was developed locally, the data pipeline was deployed to AWS cloud environment (RSD, EC2 and S3).</font></li>
<br>  
</ol>







<h1>4- Machine Learning models</h1>

<br>
<p><font size="3">A detailed technical step-by-step of solution development can be checked in the attached notebooks (development branch). Going straight to Machine Learning, the corresponding models evaluated were:</font></p>


<ul>
  <li><font size="3">KMeans</font></li>
  <li><font size="3">Gaussian Mixture Model (GMM)</font></li>
  <li><font size="3">Hierarchical clustering</font></li>
  <li><font size="3">DBSCAN</font></li>
</ul>


<p><font size="3">First, models were applied to feature space followed by embedding space generated by a fitted Random Forest Regressor dimentionally reduced by UMAP algorithm. To evaluate the quality of the generated clusters metrics such as Silhouette score (SS) and within-cluster sum of square (WSS) as well as the number of observations of each cluster were carefully considered. Kmeans applied to embedding space generated by the fitted Random Forest dimentionally reduced by UMAP was the one that better satisfied both algorithm and business requirements.</font></p>

<img src="https://drive.google.com/uc?export=view&id=1ruToMh6lLToKZlV6q7CaIIqVGJgjNbRp" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />





<h1>5- Insights about Golden customers</h1>

<br>
<p><font size="3">From the clusters provided by KMeans it was possible to sort them by its gross revenue making it easy to label the Golden customers group (the cluster with the highest gross revenue amount - cluster 4) and get key information about this group.</font></p>


<ul>
  <li><font size="3">Number of customers: 1841 (66.0%)</font></li>
  <li><font size="3">Mean recency: 19 days</font></li>
  <li><font size="3">Mean gross revenue: 3732.01 dollars</font></li>
  <li><font size="3">% of total revenue: 61</font></li>
  <li><font size="3">Mean purchase by customer: 7</font></li>
  <li><font size="3">Mean number of returns: 43</font></li>
</ul>
<br>


<a href="https://drive.google.com/uc?export=view&id=1fgg06aA3CIsbDPedhr5nws2yUpdbnAC7"><img src="https://drive.google.com/uc?export=view&id=1fgg06aA3CIsbDPedhr5nws2yUpdbnAC7" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />
<br>




<h1>6- Model deployment</h1>

<br>

<ul>
<p><li><font size="3">After developing and testing locally the finished pipeline was successfully implemented inside AWS enviroment. Briefly, the local .csv dataset used to start the solution development is now stored in a MySQL database inside AWS RDS environment. All preprocessing steps to make data ready to be consumed by KMeans as well as the KMeans clustering itself previously ran in the local environment was then implemented inside a remote AWS EC2 server and some auxiliary files required for this step of the pipeline are provided by AWS S3 storage. Cluster information provided by KMeans is then stored in a MySQL database inside AWS RDS to be finally consumed by any data visualization tool.</font></p>
      
<p><li><font size="3">The following figure ilustrates the local development and the cloud implementation of the proposed solution.</font></p>
</ul>    
<br>    

<a href="https://drive.google.com/uc?export=view&id=1CNll9U9GdU9fNCAzWNwRYHM7RLnXkWjD"><img src="https://drive.google.com/uc?export=view&id=1CNll9U9GdU9fNCAzWNwRYHM7RLnXkWjD" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />
<br>






<h1>7- Conclusions</h1>

<br>
<p><font size="3">After applying machine learning techniques it was possible to find valuable customers for the organization. These customers are elegible to 'Golden customers program'. With each cluster well defined it is also possible for the marketing team to implement driven strategies that best fit each individual group in order to manage them and satisfy their needs increasing company profit. The direct results of implemented strategies can be monitored by any data visualization tool.</font></p>
<br>






<h1>8- Next steps/Perspectives</h1>

<br>
   
    
<ul>
  <li><font size="3">It is possible to schedule pipeline tasks in order to update the customers belonging to each cluster. We did not implemented it in this version of the solution because we do not have yet updates for input data, but it is important to mention that pipeline scheduling is possible.</font></li><br>
  <li><font size="3">With well-defined groups, sales and temporal data it is possible to forecast future sales for each group by using time series forecasting techniques such as ARIMA, SARIMA, SARIMAX, etc.</font></li>
<br>
</ul>
