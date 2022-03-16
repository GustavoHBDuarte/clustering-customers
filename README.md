<h1><b><font color="#cc0000"><i>Clustering customers </i></font></b></h1>





<h1>1- Overview and business problem</h1>

<br>
<p><font size="3">A UK-based online retail store has captured the sales data for different products for the period of one year (Nov 2016 to Dec 2017). The organization sells gifts primarily on the online platform.</br> The customers who make a purchase consume directly for themselves. There are small businesses that buy in bulk and sell to other customers through the retail outlet channel.</font></p>

<p><font size="3">The organization wants to roll out a loyalty program to the high-value customers after identification of segments, therefore it is important to find significant customers for the business who make high purchases of their favourite products. For this purpose machine learning clustering methodologies were implemented aimed to segment customers into different groups with focus on the most valuable customers (we are going to call them 'Golden' customers). The final succeded model was further sucessifully applied providing a table that can be consulted via SQL query and consumed by some data visualization tool (Metabase, Power BI, Tableau, etc). The table contains mainly the identification code as well as the cluster where each customer belongs to.</font></p>

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
<p><font size="3">Models evaluated:</font></p>


<ul>
  <li><font size="3">KMeans</font></li>
  <li><font size="3">Gaussian Mixture Model (GMM)</font></li>
  <li><font size="3">Hierarchical clustering</font></li>
  <li><font size="3">DBSCAN</font></li>
</ul>


<p><font size="3">First, models were applied to feature space followed by embedding space generated by a fitted Random Forest Regressor dimentionally reduced by UMAP algorithm. To evaluate the quality of the generated clusters metrics such as Silhouette score (SS) and within-cluster sum of square (WSS) as well as the number of observations of each cluster were carefully considered. Kmeans applied to embedding space generated by the fitted Random Forest dimentionally reduced by UMAP was the one that better satisfied both algorithm and business requirements.</font></p>

<img src="https://drive.google.com/uc?export=view&id=1ruToMh6lLToKZlV6q7CaIIqVGJgjNbRp" style="width: 650px; max-width: 100%; height: auto" title="Click to enlarge picture" />


