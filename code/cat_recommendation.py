import numpy as py
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


#converting all positive vaues to 1 and everything else to 0
"""
def my_encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


myretaildata = pd.read_excel('/home/krissrinivasan/Downloads/retail.xlsx')

myretaildata['Description'] = myretaildata['Description'].str.strip() #removes spaces from beginning and end
myretaildata.dropna(axis=0, subset=['InvoiceNo'], inplace=True) #removes duplicate invoice
myretaildata['InvoiceNo'] = myretaildata['InvoiceNo'].astype('str') #converting invoice number to be string
myretaildata = myretaildata[~myretaildata['InvoiceNo'].str.contains('C')] #remove the credit transactions

mybasket = (myretaildata[myretaildata['Country'] =="Germany"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

my_basket_sets = mybasket.applymap(my_encode_units)
my_basket_sets.drop('POSTAGE', inplace=True, axis=1) #Remove "postage" as an item

my_frequent_itemsets = apriori(my_basket_sets, min_support=0.07, use_colnames=True)

my_rules = association_rules(my_frequent_itemsets, metric="confidence", min_threshold=1)


    print (my_rules.head(20))

"""