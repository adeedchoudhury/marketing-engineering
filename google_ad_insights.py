

import logging
import StringIO
import sys
import pandas as pd
import rpy2
import csv
import io
import numpy
import datetime
from rpy2.robjects import r, pandas2ri
from io import StringIO
from googleads import adwords

#FYI in order to login, you will need to create a YAML file that contains all secret token data

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)
adwords_client = adwords.AdWordsClient.LoadFromStorage()

report_downloader = adwords_client.GetReportDownloader(version='v201802')
report = {'reportName': 'Yesterday CRITERIA_PERFORMANCE_REPORT',
              'dateRangeType': 'LAST_30_DAYS',
              'reportType': 'CAMPAIGN_PERFORMANCE_REPORT',
              'downloadFormat': 'CSV',
              'selector': { 'fields': ['Date','CampaignName','CampaignId','Impressions', 'Clicks', 'Cost'] } }

csv=report_downloader.DownloadReportAsString(
          report, skip_report_header=False, skip_column_header=False,
          skip_report_summary=False, include_zero_impressions=True)



#Transforming our data into a proper pandas dataframe

txt = csv
buffer = StringIO(txt.decode())
df = pd.read_csv(buffer)
df = df.reset_index()
new_header = df.iloc[0]
df = df[1:]
df.columns=new_header
df['Cost'] = pd.to_numeric(df['Cost'])
df['spend_actual_usd'] = df['Cost']/1000000



get_ipython().run_cell_magic(u'capture', u'', u'%%R \nrequire(ggplot2)\nrequire(scales)\nrequire(dplyr)')
get_ipython().magic(u'load_ext rpy2.ipython')
get_ipython().magic(u'R library(devtools)')
get_ipython().magic(u'R library(adjust)')
get_ipython().magic(u"R adjust.setup(user.token='XXXX', app.tokens=c('XXXX','XXXX'))")
get_ipython().run_cell_magic(u'R', u"adj_data = adjust.cohorts(start_date='2018-01-01', end_date='2019-12-01',", u"                       countries='us',\n                       kpis=c('retained_users', 'sessions_per_user', 'cohort_size','time_spent_per_user'),\n                       grouping=c('day','networks','adgroups','campaigns'))")



pandas2ri.activate()
r.data('adj_data')
adjust_data = pandas2ri.ri2py(r['adj_data'])
google_adjust_data = adjust_data.loc[adjust_data['network'] == 'Adwords UAC Installs']
google_adjust_data = google_adjust_data[google_adjust_data['period'].isin([0,1,7])]
google_adjust_data = google_adjust_data.pivot_table(index=['date','campaign'], columns='period', values=['retained_users','sessions_per_user','cohort_size','time_spent_per_user'], aggfunc=numpy.sum)
google_adjust_data = google_adjust_data.reset_index()
google_adjust_data['campaign_name'], google_adjust_data['campaign_id'] = google_adjust_data['campaign'].str.split('(', 1).str
google_adjust_data['campaign_id'], google_adjust_data['paranthesis'] = google_adjust_data['campaign_id'].str.split(')', 1).str


df['Campaign'] = df['Campaign'].astype(str)
df['Day'] = df['Day'].astype(str)

google_master_data = pd.merge(google_adjust_data, df,
                          how='left',
                          left_on=['campaign_id','date'],
                          right_on=['Campaign ID','Day'])

google_pivot = google_master_data.rename(columns={('retained_users', 1.0): 'd1_retained',
                                          ('retained_users', 7.0): 'd7_retained',
                                          ('retained_users', 0.0): 'adjust_installs',
                                          ('campaign_name', ''): 'campaign_name',
                                          ('date', ''): 'date'})


google_pivot = google_pivot[['date',
          'campaign_name',
          'Clicks',
          'Impressions',
          'spend_actual_usd',       
          'adjust_installs',
          'd1_retained',
          'd7_retained']]


google_pivot= google_pivot[pd.notnull(google_pivot['Impressions'])]


google_now = datetime.datetime.now()
concat = 'google_master_data_final -'+str(google_now)+'.csv'
csv_file = google_pivot.to_csv(concat, encoding='utf-8', index=False)
