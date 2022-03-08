# Library imports

import pandas as pd
import numpy as np
import warnings
import inflection
import re
import pymysql
import pickle
import boto3
import boto3.session
import s3fs
from datetime         import datetime
from sqlalchemy       import create_engine
from sklearn.cluster  import KMeans
from sklearn.metrics  import silhouette_score
from sklearn.ensemble import RandomForestRegressor
import umap.umap_ as umap


# Loading data ===========================================================================

db_credentials = pd.read_csv('s3://gustavoawsbucketds/db_credentials.txt', header=None)


# DB creentials

user = db_credentials[0][0]
psw = db_credentials[1][0]
host = db_credentials[2][0]
port = db_credentials[3][0]
schema = db_credentials[4][0]
schema_2 = db_credentials[5][0]



# Selecting data from database - SQL query ('purchases' table - ecommerce schema)

query = """
    SELECT *
    FROM purchases

"""

# creating the conection to existing db
connection = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, psw, host, port, schema))

# executing sql query
df = pd.read_sql_query(query, con=connection)

# closing database connection
connection.dispose()


# 1 - Data description ========================================================================


# Adjusting column names

df.columns = list(map(lambda x: inflection.underscore(x), df.columns)) #changing to underscore + lower(snakecase)

# Replaca NA's

df = df.dropna(subset=['description', 'customer_id'])


# Changing data types 

# Changing column 'invoice_date' to datetime

df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%b-%y')


# Changing column 'customer_id' to int

df['customer_id'] = df['customer_id'].astype(int)


# 2 - Data filtering ========================================================================


# Removing inconsistencies


# 'unit_price' column:

# we are going to ignore 'unit_price'==0. We will consider 'unite_price'>0.04

df = df.loc[df['unit_price']>0.04, :]



# 'stock_code' column:

# removing the rows where the values are one of these: ['POST' 'D' 'M' 'PADS' 'DOT' 'CRUK']
df = df.loc[~df['stock_code'].isin(['POST' 'D' 'M' 'PADS' 'DOT' 'CRUK'])]




# 'description' column:

# removing 'description' column assuming it does not have relevance information
df = df.drop(columns='description')




# 'country' column (map)

# removing rows where 'country' == 'European Community', 'Unspecified'
df = df.loc[~df['country'].isin(['European Community', 'Unspecified']), :]






# 'quantity' column:

# getting a dataframe with only returns operations
df_2_returns = df.loc[df['quantity'] < 0, :]

# getting a dataframe with only purchases operations
df_2_purchases = df.loc[df['quantity'] >= 0, :]






# Removing inconsistencies in observations:


# based on previous univariate analysis, we investigated for some potential outliers (customers with unusual purchase behaviour)

## we are going to remove these observations




# 'customer_id' == 16446 (this customer had two records that do not represent actual purchases, and 2 more records with only 1 item purchased each)
## should be removed because this customer is generating distortion in the avg_ticket calculation

df_2_purchases = df_2_purchases[~df_2_purchases['customer_id'].isin([16446])]



# ***********************************************

# Saving cleaned purchases table into a sql database to be further consumed by an external visualization tool via sql query



# creating the conection to existing db
connection = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(user, psw, host, port, schema_2))

# inserting data to database
df_2_purchases.to_sql( 'purchases', con=connection, if_exists='append', index=False)

# ***********************************************

# closing database connection
connection.dispose()







# 3 - Feature engineering ========================================================================


# Feature creation


# Creating reference dataframe

df_ref = df.drop(['invoice_no', 'stock_code', 'quantity', 'invoice_date',
                   'unit_price', 'country'], axis=1).drop_duplicates(ignore_index=True)


# Creating 'gross_revenue' column to df_2_purchases (gross_revenue = unit_price * quantity)

df_2_purchases['gross_revenue'] = df_2_purchases['unit_price'] * df_2_purchases['quantity']



# Monetary (grouping 'gross_revenue' by customer)

df_monetary = df_2_purchases[['customer_id', 'gross_revenue']].groupby('customer_id').sum().reset_index()


# Joining df_ref and df_monetary

df_ref = pd.merge(left=df_ref, right=df_monetary, how='left', on='customer_id')








# Recency - last day purchase (grouping 'invoice_date' by customer and getting de max date)

df_recency = df_2_purchases[['customer_id', 'invoice_date']].groupby('customer_id').max().reset_index() # creating df_recency

df_recency['recency'] = df_2_purchases['invoice_date'].max() - df_recency['invoice_date'] # adding 'recency' column (last purchase day of each customer - max day of dataset)

df_recency['recency'] = df_recency['recency'].apply( lambda x: x.days) # extrating the number of days (from X days)


# Joining df_ref and df_recency

df_ref = pd.merge(left=df_ref, right=df_recency[['customer_id','recency']], how='left', on='customer_id')








# Quantity of purchases by costumer - purchase frequency of each customer

df_purch_cost = df_2_purchases[['customer_id','invoice_no']].drop_duplicates().groupby('customer_id').count().reset_index()
df_purch_cost.columns = ['customer_id', 'purchase_by_costumer'] # renaming column 'invoice' to 'purchase_by_costumer'


# Joining df_ref and df_purch_cost

df_ref = pd.merge(left=df_ref, right=df_purch_cost, how='left', on='customer_id')








# Number of items purchased

df_total_purchased = df_2_purchases[['customer_id','quantity']].groupby('customer_id').sum().reset_index()
df_total_purchased.columns = ['customer_id', 'number_items_purchased'] # renaming column 'invoice' to 'purchase_by_costumer'


# Joining df_ref and df_total_purchased

df_ref = pd.merge(left=df_ref, right=df_total_purchased, how='left', on='customer_id')








# Number of products purchased

df_total_products = df_2_purchases[['customer_id','stock_code']].groupby('customer_id').count().reset_index()
df_total_products.columns = ['customer_id', 'number_products_purchased'] # renaming column 'invoice' to 'purchase_by_costumer'


# Joining df_ref and df_total_purchased

df_ref = pd.merge(left=df_ref, right=df_total_products, how='left', on='customer_id')








# Average ticket - mean purchase amount

df_avg_ticket = df_2_purchases[['customer_id','gross_revenue']].groupby('customer_id').mean().reset_index()
df_avg_ticket.columns = ['customer_id', 'avg_ticket']


# Joining df_ref and df_avg_ticket

df_ref = pd.merge(left=df_ref, right=df_avg_ticket, how='left', on='customer_id')








# Average period between purchases


df_aux = df_2_purchases[['customer_id', 'invoice_date']].drop_duplicates().sort_values(['customer_id','invoice_date'],
                                                                             ascending=['False', 'False'])

df_aux['previous_costumer_id'] = df_aux['customer_id'].shift() #getting next row's custumer_id

df_aux['previous_invoice_date'] = df_aux['invoice_date'].shift() #getting next row's invoice_date


df_aux['recency_days'] = df_aux.apply(lambda x: (x['invoice_date'] - x['previous_invoice_date']).days +1 
                                                    if x['customer_id'] == x['previous_costumer_id'] else np.nan, axis=1)

df_aux = df_aux.drop(columns=['invoice_date', 'previous_costumer_id', 'previous_invoice_date']) # droping auxiliary columns 

df_aux = df_aux.dropna() # droping Na's

df_avg_recency_days = df_aux.groupby('customer_id').mean().reset_index()

df_avg_recency_days.columns = ['customer_id', 'mean_recency_days']



# Joining df_ref and df_avg_recency_days

df_ref = pd.merge(left=df_ref, right=df_avg_recency_days, how='left', on='customer_id')








# Frequency purchase (mean of unique purchases/time interval between the first and the last purchase)


df_aux = (df_2_purchases[['customer_id', 'invoice_no', 'invoice_date']].drop_duplicates()
                                                                       .groupby('customer_id')
                                                                       .agg(max_ = ('invoice_date', 'max'),
                                                                            min_ = ('invoice_date', 'min'),
                                                                            days_ = ('invoice_date', lambda x: (((x.max()-x.min()).days)+1)),
                                                                            buy_ = ('invoice_no', 'count'))).reset_index()

df_aux['frequency'] = df_aux[['days_', 'buy_']].apply(lambda x: x['buy_']/x['days_'] if x['days_'] != 0 else 0 , axis=1)




# Joining df_ref and df_aux

df_ref = pd.merge(left=df_ref, right=df_aux[['frequency', 'customer_id']], how='left', on='customer_id')








# Returns - number of returns

df_ret = (df_2_returns[['customer_id', 'quantity']].groupby('customer_id')
                                                   .sum()
                                                   .reset_index()
                                                   .drop_duplicates()
                                                   .rename(columns={'quantity':'number_of_returns'}))
 
df_ret['number_of_returns'] = df_ret['number_of_returns']*-1 # getting positive values



# Joining df_ref and df_ret

df_ref = pd.merge(left=df_ref, right=df_ret, how='left', on='customer_id')
df_ref['number_of_returns'].fillna(0, inplace=True) # filling 'number_of_returns' with zero (when customer have never returned a product purchased)








# Basket size - mean quantity (sum) of products in each purchase by costumer



df_aux = (df_2_purchases[['customer_id', 'invoice_no', 'quantity']].groupby('customer_id')
                                                                   .agg(n_purchases=('invoice_no', 'nunique'),
                                                                        n_products=('quantity', 'sum'))
                                                                   .reset_index())

df_aux['avg_basket_size'] = df_aux['n_products']/df_aux['n_purchases'] # calculating avg basket size of each customer



# Joining df_ref and df_aux

df_ref = pd.merge(left=df_ref, right=df_aux[['customer_id','avg_basket_size']], how='left', on='customer_id')








# Basket size unique - mean quantity (sum) of unique products in each purchase by costumer



df_aux = (df_2_purchases[['customer_id', 'invoice_no', 'stock_code']].groupby('customer_id')
                                                                     .agg(n_purchases=('invoice_no', 'nunique'),
                                                                          n_products=('stock_code', 'count'))
                                                                     .reset_index())

df_aux['avg_unique_basket_size'] = df_aux['n_products']/df_aux['n_purchases'] # calculating avg basket size of each customer



# Joining df_ref and df_aux

df_ref = pd.merge(left=df_ref, right=df_aux[['customer_id','avg_unique_basket_size']], how='left', on='customer_id')






# 5 - Data preparation ========================================================================


#droping NA's generated from the previous step:
df_ref = df_ref.dropna()


# Tree-based embedding:


# defining 'gross_revenue' as target variable

y = df_ref['gross_revenue']

X = df_ref.drop(columns='gross_revenue')
X = X.set_index('customer_id')


# Loading tree model from AWS S3

# getting bucket name
for bucket_name in boto3.resource('s3').buckets.all():
    bucket_name = bucket_name.name


# getting credentials
cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key

s3client = boto3.client('s3', 
                        aws_access_key_id = ACCESS_KEY, 
                        aws_secret_access_key = SECRET_KEY
                       )
#responde
response = s3client.get_object(Bucket=bucket_name, Key='rf_model.pkl')

body = response['Body'].read()

#tree
rf = pickle.loads(body)


# getting leaf information
leaf = rf.apply(X)

# df leaf
df_leaf = pd.DataFrame(leaf)



# Applying UMAP to tree-embedded data


# loading fitted reducer from AWS S3

# getting bucket name
for bucket_name in boto3.resource('s3').buckets.all():
    bucket_name = bucket_name.name


# getting credentials
cred = boto3.Session().get_credentials()
ACCESS_KEY = cred.access_key
SECRET_KEY = cred.secret_key

s3client = boto3.client('s3', 
                        aws_access_key_id = ACCESS_KEY, 
                        aws_secret_access_key = SECRET_KEY
                       )
#response
response = s3client.get_object(Bucket=bucket_name, Key='reducer_umap.pkl')

body = response['Body'].read()

#embedding
reducer_umap = pickle.loads(body)

embedding = reducer_umap.transform(df_leaf)

# getting axis for plot and clustering
df_tree_umap = pd.DataFrame()
df_tree_umap['embeddings_x'] = embedding[:,0]
df_tree_umap['embeddings_y'] = embedding[:,1]




# 8 - Model training ========================================================================


# K-Means

# K-Means with tree-based embeddings


# Model

k = 11


# instantiating the model

model_embedded = KMeans(init='random', n_clusters=k, n_init=10, max_iter=300, random_state=42)


# fitting the model

model_embedded.fit(df_tree_umap)


# predicting labels/clusters

labels_embedded = model_embedded.labels_


# Cluster validation


# Embedded model - metrics
print('Kmeans metrics:\n')

# WSS
print('WSS: {:.2f}'.format(model_embedded.inertia_))

# SS
print('Silhouette score: {:.2f}'.format(round(silhouette_score(df_tree_umap, labels_embedded, metric='euclidean', random_state=42),2)))



# 9 - Cluster analysis ========================================================================


# Adding embedded 'cluster/label' column to df_4_2 (df_4 without data transforming. For cluster profile report)


df_ref['label'] = labels_embedded+1


# Renaming the best cluster to "Golden"

# getting cluster number of the Golden group
cluster_number = df_ref[['gross_revenue', 'label']].groupby('label').mean().reset_index().sort_values(by='gross_revenue', ascending=False).iloc[0,0]

# replacing the cluster number to 'Golden'
df_ref.loc[df_ref['label']==cluster_number, 'label'] = 'Golden'

# droping mean-related columns
df_ref = df_ref.drop(columns=['avg_ticket', 'mean_recency_days', 'avg_basket_size', 'avg_unique_basket_size'])


# changing data types
df_ref['recency'] = df_ref['recency'].astype('int')

df_ref['purchase_by_costumer'] = df_ref['purchase_by_costumer'].astype('int')

df_ref['number_items_purchased'] = df_ref['number_items_purchased'].astype('int')

df_ref['number_products_purchased'] = df_ref['number_products_purchased'].astype('int')

df_ref['number_of_returns'] = df_ref['number_of_returns'].astype('int')


# adding 'last_training_timestamp' column
df_ref['last_training_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
df_ref['last_training_timestamp'] = pd.to_datetime(df_ref['last_training_timestamp'], format='%Y-%m-%d %H:%M:%S')



# ***********************************************

# Inserting data to sql database using SQLAlchemy (SQLAlchemy is able to insert data into several databases)

# creating the conection to existing db
connection = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(user, psw, host, port, schema_2))

# inserting data to database
df_ref.to_sql( 'customers', con=connection, if_exists='append', index=False)


# ***********************************************

# closing database connection
connection.dispose()
