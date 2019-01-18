from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads.http import Request
from twitter_ads.error import Error
from numpy import base_repr
import time
import pandas as pd
import json
from datetime import datetime, timedelta
import datetime
import rpy2
from rpy2.robjects import r, pandas2ri
import numpy

from twitter_ads.campaign import LineItem
from twitter_ads.enum import METRIC_GROUP
from twitter_ads.enum import GRANULARITY

#Initializing Account and identifying campaigns id's that I would like to pull

CONSUMER_KEY = 'XXXX'
CONSUMER_SECRET = 'XXXX'
ACCESS_TOKEN = 'XXXX'
ACCESS_TOKEN_SECRET = 'XXXX'
ACCOUNT_ID='XXXX'

client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
account = client.accounts(ACCOUNT_ID)
metric_groups = ["BILLING","ENGAGEMENT"]
resource = '/2/stats/accounts/18ce53wxop6/'.format(account_id=account.id)

line_items = list(account.line_items(None, count=20))[:20]
cids = ['XXXX', 'XXXX']


#Creating some dates for reference

today = datetime.datetime.now()
DD_7 = datetime.timedelta(days=7)
DD_14 = datetime.timedelta(days=14)
earlier = today - DD_7
last_2w = today-DD_14
start_date = earlier.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")
last_2w = last_2w.strftime("%Y-%m-%d")

# First For Loop to collect last_7_day data

appended_data = []
for x in cids:
    #Performing Response
    params1 = {"entity" : "CAMPAIGN", "entity_ids" : x,
              "start_time" : start_date, "end_time" : end_date,
              "granularity" : "DAY", "placement" : "ALL_ON_TWITTER",
              "metric_groups" : ["BILLING","ENGAGEMENT"], "country": "us"}
    params2 = {"entity" : "CAMPAIGN", "entity_ids" : x,
              "start_time" : start_date, "end_time" : end_date,
              "granularity" : "DAY", "placement" : "ALL_ON_TWITTER",
              "metric_groups" : ["ENGAGEMENT"], "country": "us"}
    response1 = Request(client, 'get', resource, params=params1).perform()
    response2 = Request(client, 'get', resource, params=params2).perform()

    #Response Data
    spend_data = response1.body
    engagement_data = response2.body

    #Spend Data
    df = pd.DataFrame(spend_data['data'])
    id_value = df['id']
    id_value = pd.DataFrame(id_value)
    id_value = str(id_value)
    id_value = id_value[12:]
    df1 = pd.DataFrame(json.loads(df["id_data"].to_json(orient="records")))
    df2 = pd.DataFrame(json.loads(df1[0].to_json(orient="records")))
    df3 = pd.DataFrame(json.loads(df2["metrics"].to_json(orient="records")))
    df4 = pd.DataFrame(df3)
    df_spend = df4.billed_charge_local_micro.values.tolist()
    df_installs = df4.billed_engagements.values.tolist()
    df_spend = pd.DataFrame(df_spend)
    df_installs = pd.DataFrame(df_installs)
    df_spend= df_spend.transpose()
    df_installs = df_installs.transpose()
    df_spend.rename(columns = {list(df_spend)[0]: 'spend'}, inplace = True)
    df_installs.rename(columns = {list(df_installs)[0]: 'clicks'}, inplace = True)
    df_spend['spend_actual_yen'] = (df_spend['spend']/1000000)
    df_spend['spend_actual_usd']=df_spend['spend_actual_yen']/105
    df_spend.insert(0,'campaign',id_value)
    billed_data = df_spend.join(df_installs)
    billed_data

    #Time Range
    from datetime import date, timedelta, datetime

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    delta = end_dt - start_dt        # timedelta

    dates = []
    for i in range(delta.days + 1):
       dates.append(start_dt + timedelta(days=i))

    dates = pd.DataFrame(dates)
    dates.rename(columns = {list(dates)[0]: 'date'}, inplace = True)
    dates = dates.drop(dates.index[len(dates)-1])
    final_billed = dates.join(billed_data)
    final_billed

    #Twitter Stats
    bf = pd.DataFrame(engagement_data['data'])
    bf1 = pd.DataFrame(json.loads(bf["id_data"].to_json(orient="records")))
    bf2 = pd.DataFrame(json.loads(bf1[0].to_json(orient="records")))
    bf3 = pd.DataFrame(json.loads(bf2["metrics"].to_json(orient="records")))
    bf4 = pd.DataFrame(bf3)
    df_follows = bf4.follows.tolist()
    df_impressions = bf4.impressions.values.tolist()
    df_clicks = bf4.app_clicks.values.tolist()
    df_retweets = bf4.retweets.values.tolist()
    df_follows = pd.DataFrame(df_follows).transpose()
    df_impressions = pd.DataFrame(df_impressions).transpose()
    df_retweets = pd.DataFrame(df_retweets).transpose()
    df_clicks = pd.DataFrame(df_clicks).transpose()
    df_follows.rename(columns = {list(df_follows)[0]: 'follows'}, inplace = True)
    df_impressions.rename(columns = {list(df_impressions)[0]: 'impressions'}, inplace = True)
    df_retweets.rename(columns = {list(df_retweets)[0]: 'retweets'}, inplace = True)
    df_clicks.rename(columns = {list(df_clicks)[0]: 'clicks_actual'}, inplace = True)
    combined_data = df_retweets.join(df_impressions)
    combined_data_final = combined_data.join(df_follows)
    final_twitter = final_billed.join(combined_data_final)
    final_twitter_v2 = final_twitter.join(df_clicks)
    appended_data.append(final_twitter_v2)

# Second For Loop to collect data from the week prior

appended_data_v2 = []
for x in cids:
    #Performing Response
    params1 = {"entity" : "CAMPAIGN", "entity_ids" : x,
              "start_time" : last_2w, "end_time" : start_date,
              "granularity" : "DAY", "placement" : "ALL_ON_TWITTER",
              "metric_groups" : ["BILLING","ENGAGEMENT"], "country": "us"}
    params2 = {"entity" : "CAMPAIGN", "entity_ids" : x,
              "start_time" : last_2w, "end_time" : start_date,
              "granularity" : "DAY", "placement" : "ALL_ON_TWITTER",
              "metric_groups" : ["ENGAGEMENT"], "country": "us"}
    response1 = Request(client, 'get', resource, params=params1).perform()
    response2 = Request(client, 'get', resource, params=params2).perform()

    #Response Data
    spend_data = response1.body
    engagement_data = response2.body

    #Spend Data
    df = pd.DataFrame(spend_data['data'])
    id_value = df['id']
    id_value = pd.DataFrame(id_value)
    id_value = str(id_value)
    id_value = id_value[12:]
    df1 = pd.DataFrame(json.loads(df["id_data"].to_json(orient="records")))
    df2 = pd.DataFrame(json.loads(df1[0].to_json(orient="records")))
    df3 = pd.DataFrame(json.loads(df2["metrics"].to_json(orient="records")))
    df4 = pd.DataFrame(df3)
    df_spend = df4.billed_charge_local_micro.values.tolist()
    df_installs = df4.billed_engagements.values.tolist()
    df_spend = pd.DataFrame(df_spend)
    df_installs = pd.DataFrame(df_installs)
    df_spend= df_spend.transpose()
    df_installs = df_installs.transpose()
    df_spend.rename(columns = {list(df_spend)[0]: 'spend'}, inplace = True)
    df_installs.rename(columns = {list(df_installs)[0]: 'clicks'}, inplace = True)
    df_spend['spend_actual_yen'] = (df_spend['spend']/1000000)
    df_spend['spend_actual_usd']=df_spend['spend_actual_yen']/105
    df_spend.insert(0,'campaign',id_value)
    billed_data = df_spend.join(df_installs)
    billed_data

    #Time Range
    from datetime import date, timedelta, datetime

    start_dt = datetime.strptime(last_2w, "%Y-%m-%d")
    end_dt = datetime.strptime(start_date, "%Y-%m-%d")

    delta = end_dt - start_dt        # timedelta

    dates = []
    for i in range(delta.days + 1):
       dates.append(start_dt + timedelta(days=i))

    dates = pd.DataFrame(dates)
    dates.rename(columns = {list(dates)[0]: 'date'}, inplace = True)
    dates = dates.drop(dates.index[len(dates)-1])
    final_billed = dates.join(billed_data)
    final_billed

    #Twitter Stats
    bf = pd.DataFrame(engagement_data['data'])
    bf1 = pd.DataFrame(json.loads(bf["id_data"].to_json(orient="records")))
    bf2 = pd.DataFrame(json.loads(bf1[0].to_json(orient="records")))
    bf3 = pd.DataFrame(json.loads(bf2["metrics"].to_json(orient="records")))
    bf4 = pd.DataFrame(bf3)
    df_follows = bf4.follows.tolist()
    df_impressions = bf4.impressions.values.tolist()
    df_clicks = bf4.app_clicks.values.tolist()
    df_retweets = bf4.retweets.values.tolist()
    df_follows = pd.DataFrame(df_follows).transpose()
    df_impressions = pd.DataFrame(df_impressions).transpose()
    df_retweets = pd.DataFrame(df_retweets).transpose()
    df_clicks = pd.DataFrame(df_clicks).transpose()
    df_follows.rename(columns = {list(df_follows)[0]: 'follows'}, inplace = True)
    df_impressions.rename(columns = {list(df_impressions)[0]: 'impressions'}, inplace = True)
    df_retweets.rename(columns = {list(df_retweets)[0]: 'retweets'}, inplace = True)
    df_clicks.rename(columns = {list(df_clicks)[0]: 'clicks_actual'}, inplace = True)
    combined_data = df_retweets.join(df_impressions)
    combined_data_final = combined_data.join(df_follows)
    final_twitter = final_billed.join(combined_data_final)
    final_twitter_v2 = final_twitter.join(df_clicks)
    appended_data_v2.append(final_twitter_v2)

 # Merging tables into 1 dataframe

twitter_stats = pd.concat(appended_data)
twitter_stats_v2 = pd.concat(appended_data_v2)
twitter_stats = pd.concat([twitter_stats, twitter_stats_v2])
twitter_stats = twitter_stats.sort_values(['spend_actual_usd'], ascending=False)

# Collecting Adjust Data

get_ipython().run_cell_magic(u'capture', u'', u'%%R \nrequire(ggplot2)\nrequire(scales)\nrequire(dplyr)')
get_ipython().magic(u'load_ext rpy2.ipython')
get_ipython().magic(u'R library(devtools)')
get_ipython().magic(u'R library(adjust)')
get_ipython().magic(u"R adjust.setup(user.token='XXXX', app.tokens=c('XXXX','XXXX'))")
get_ipython().run_cell_magic(u'R', u"adj_data = adjust.cohorts(start_date='2018-01-01', end_date='2019-12-01',", u"countries='us',\n                         kpis=c('retained_users', 'sessions_per_user', 'cohort_size','time_spent_per_user'),\n                         grouping=c('day','networks','adgroups','campaigns'))")

#Putting Adjust data into a Pandas dataframe and filtering for D1 and D7 information

pandas2ri.activate()
r.data('adj_data')
adjust_data = pandas2ri.ri2py(r['adj_data'])
twitter_adjust_data = adjust_data.loc[adjust_data['network'] == 'Twitter Installs']
twitter_adjust_data = twitter_adjust_data[twitter_adjust_data['period'].isin([0,1,7])]
twitter_adjust_data = twitter_adjust_data.pivot_table(index=['date','adgroup','campaign'], columns='period', values=['retained_users','sessions_per_user','cohort_size','time_spent_per_user'], aggfunc=numpy.sum)
twitter_adjust_data = twitter_adjust_data.reset_index()
twitter_adjust_data['campaign_name'], twitter_adjust_data['campaign_id'] = twitter_adjust_data['campaign'].str.split(' ', 1).str
twitter_adjust_data['campaign_id']=twitter_adjust_data['campaign_id'].str[1:6]

#Data conversions for merging

twitter_stats['campaign'] = twitter_stats['campaign'].astype(str)
twitter_stats['date'] = twitter_stats['date'].astype(str)

#Merging data and data cleaning

twitter_master_data = pd.merge(twitter_stats, twitter_adjust_data,
                          how='left',
                          right_on=['campaign_id','date'],
                          left_on=['campaign','date'])

twitter_master_data= twitter_master_data[pd.notnull(twitter_master_data['impressions'])]

twitter_pivot = twitter_master_data.rename(columns={('retained_users', 1.0): 'd1_retained',
                                          ('retained_users', 7.0): 'd7_retained',
                                          ('retained_users', 0.0): 'adjust_installs',
                                          ('campaign_name', ''): 'campaign_name',
                                          ('date', ''): 'date1'})

twitter_pivot = twitter_pivot[['date',
          'campaign_name',
          'clicks',
          'clicks_actual',
          'impressions',
          'spend_actual_usd',
          'retweets',
          'follows',           
          'adjust_installs',
          'd1_retained',
          'd7_retained']]

twitter_agg = twitter_pivot.groupby(['date', 'campaign_name', 'clicks_actual','impressions','spend_actual_usd','retweets','follows']).agg({'adjust_installs':'sum', 'd1_retained':'sum', 'd7_retained':'sum'}).reset_index()

# Creating CSV file from final dataframe that combines Adjust data and Twitter API data

twitter_now = datetime.datetime.now()
concat = 'twitter_master_data_final -'+str(twitter_now)+'.csv'
csv_file = twitter_agg.to_csv(concat, encoding='utf-8', index=False)



