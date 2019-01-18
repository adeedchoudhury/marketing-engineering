import datetime
import csv
import pandas as pd
import numpy as np
import rpy2

from facebookads.api import FacebookAdsApi
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.business import Business
from facebookads.adobjects.adasyncrequestset import AdAsyncRequestSet
from facebookads.adobjects.adasyncrequest import AdAsyncRequest
from facebookads.adobjects.adreportrun import AdReportRun
from rpy2.robjects import r, pandas2ri

#Async Job

def wait_for_async_job(job):
    for _ in range(1000):
        time.sleep(1)
        job = job.remote_read()
        status = job[AdReportRun.Field.async_status]
        if status == "Job Completed":
            return job.get_result(params={"limit": 1000})



#Authentication and Fields

my_app_id = 'XXXX'
my_app_secret = 'XXXX'
my_access_token = 'XXXX'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

business = Business('XXXX')
accounts = business.get_owned_ad_accounts(fields=[AdAccount.Field.id])
account = AdAccount('XXXX')

fields = [AdsInsights.Field.account_id,
           AdsInsights.Field.account_name,
           AdsInsights.Field.ad_id,
           AdsInsights.Field.ad_name,
           AdsInsights.Field.adset_id,
           AdsInsights.Field.adset_name,
           AdsInsights.Field.campaign_id,
           AdsInsights.Field.campaign_name,
           AdsInsights.Field.actions,
           AdsInsights.Field.action_values,
           AdsInsights.Field.relevance_score,
           AdsInsights.Field.total_actions,
           AdsInsights.Field.spend,
           AdsInsights.Field.clicks,
           AdsInsights.Field.cpm,
           AdsInsights.Field.impressions,
           AdsInsights.Field.frequency,
           AdsInsights.Field.objective,
           AdsInsights.Field.reach,
           AdsInsights.Field.date_start,
           AdsInsights.Field.date_stop
           ]
params = {
'level': 'ad',
'time_increment': 1,
'limit':'1000'
}

#Collecting Job Data


job = account.get_insights_async(params=params, fields=fields)
result_cursor = wait_for_async_job(job)
results = [item for item in result_cursor]
results = pd.DataFrame(results)
results['actiontype'] = results.apply(lambda row: type(row['actions']),axis=1)
results2 = results[results['actiontype']==list]
results3 = results2.copy()
#Unpacking Columns

actions_types = ['like','mobile_app_install','comment','app_custom_event.fb_mobile_content_view']
for i in action_types:
  results3.loc[:,i] = results3.apply(lambda row: [y['value'] for y in row['actions'] if y['action_type'] == i], axis=1)
  results3[i] = results3[i].str[0]

fb_stats = results3.fillna(0)

#Converting Data Types + some calculated fields

stats = ['spend','like','mobile_app_install','comment','app_custom_event.fb_mobile_content_view','reach','total_actions','impressions','clicks']

for i in stats:
  fb_stats[i] = fb_stats[i].astype(float)

merged_values = ['adset_id','ad_id','date_start']

for i in merged_values:
  fb_stats[i] = fb_stats[i].astype(str)


fb_stats['CPI'] = fb_stats['spend']/fb_stats['install_action']
fb_stats['CPM'] = fb_stats['spend']/(fb_stats['impressions']/1000)
fb_stats['CTR'] = fb_stats['clicks']/fb_stats['impressions']
fb_stats['eCVR'] = fb_stats['install_action']/fb_stats['impressions']

fb_stats['date_start']=pd.to_datetime(fb_stats['date_start'])
fb_stats['date_stop']=pd.to_datetime(fb_stats['date_stop'])

#Collecting Adjust Data


get_ipython().run_cell_magic(u'capture', u'', u'%%R \nrequire(ggplot2)\nrequire(scales)\nrequire(dplyr)')
get_ipython().magic(u'load_ext rpy2.ipython')
get_ipython().magic(u'R library(devtools)')
get_ipython().magic(u'R library(adjust)')
get_ipython().magic(u"R adjust.setup(user.token='XXXX', app.tokens=c('XXXX','XXXX))")
get_ipython().run_cell_magic(u'R', u"df1 = adjust.cohorts(start_date='2018-01-01', end_date='2019-12-01',", u"                         countries='us',\n                         kpis=c('retained_users', 'sessions_per_user', 'cohort_size','time_spent_per_user'),\n                         grouping=c('day','networks','adgroups','campaigns','creatives'))")
get_ipython().magic(u'R df1')

pandas2ri.activate()
r.data('df1')
adjust_data = pandas2ri.ri2py(r['df1'])
fb_adjust_data = adjust_data.loc[adjust_data['network'].isin(['Instagram Installs', 'Facebook Installs','Off-Facebook Installs'])]
fb_adjust_data = fb_adjust_data[fb_adjust_data['period'].isin([0,1,7])]
fb_adjust_data = fb_adjust_data.pivot_table(index=['date','adgroup','campaign','creative'], columns='period', values=['retained_users','sessions_per_user','cohort_size','time_spent_per_user'], aggfunc=np.sum)
fb_adjust_data = fb_adjust_data.reset_index()


# Doing some data cleaning on adgroup and campaign name; seperating our the adset id from the adset name and the campaign id from the campaign name

fb_adjust_data['AdSet_name'], fb_adjust_data['AdSet_ID'] = fb_adjust_data['adgroup'].str.split(' ', 1).str
fb_adjust_data['creative_name'], fb_adjust_data['creative_id'] = fb_adjust_data['creative'].str.split('(', 1).str
fb_adjust_data['creative_id'], fb_adjust_data['paranthesis'] = fb_adjust_data['creative_id'].str.split(')', 1).str
fb_adjust_data['AdSet_ID']=fb_adjust_data['AdSet_ID'].str[1:18]
fb_adjust_data.loc['AdSet_ID'] = pd.to_numeric(fb_adjust_data['AdSet_ID'], errors='coerce')


#Merging the adjust data w/ the fb_stats data

fb_master_data = pd.merge(fb_adjust_data, fb_stats,
                          how='left',
                          left_on=['AdSet_ID','creative_id', 'date'],
                          right_on=['adset_id','ad_id','date_start'])


#Renaming some columns on the final table and saving it as a different name

fb_pivot = fb_master_data.rename(columns={('retained_users', 1.0): 'd1_retained',
                                          ('retained_users', 7.0): 'd7_retained',
                                          'mobile_app_install': 'fb_installs',
                                          ('retained_users', 0.0): 'adjust_installs',
                                          'app_custom_event.fb_mobile_content_view':'articles_read',
                                          'comment': 'comments',
                                          ('creative_name', ''): 'creative',
                                          ('date', ''): 'date'})

fb_pivot = fb_pivot[['date',
          'campaign_name',
          'adset_name',
          'creative',
          'clicks',
          'impressions',
          'spend',
          'comments',
          'articles_read',
          'fb_installs',
          'adjust_installs',
          'd1_retained',
          'd7_retained']]


fb_pivot = fb_pivot[pd.notnull(fb_pivot['impressions'])]

#To create final data dump

fb_now = datetime.datetime.now()
concat = 'fb_master_data_final -'+str(fb_now)+'.csv'
csv_file = fb_pivot.to_csv(concat, encoding='utf-8', index=False)






