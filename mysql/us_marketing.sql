CREATE TABLE daily_stats_digital_turbine (
  date date NOT NULL COMMENT 'Date of the metric. Note that this is in EST.',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "digital_turbine")',
  campaign_name varchar(300) NOT NULL COMMENT 'Name of the campaign',
  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign',
  spend double unsigned NOT NULL COMMENT 'Spend',
  install_count bigint(20) unsigned NOT NULL COMMENT 'Number of installs',
  preload_count bigint(20) unsigned NOT NULL COMMENT 'Number of preloads',
  click_count bigint(20) unsigned NOT NULL COMMENT 'Number of clicks',
  country_code varchar(20) NOT NULL COMMENT 'Country code in which the campaign took place',
  cpi double unsigned NOT NULL COMMENT 'Cost Per Install (CPI)',
  ctr double unsigned COMMENT 'Click Through Rate (CTR). Note that this can be null',
  UNIQUE KEY idx1 (date, network, campaign_id, country_code)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='Digital Turbine-related metrics. See https://digitalturbine.atlassian.net/wiki/spaces/PDS/pages/36208899/Advertiser+Reports+API'
;

CREATE TABLE daily_stats_iron_source (
  date date NOT NULL COMMENT 'Date of the metric in UTC',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "iron_source")',
  campaign_name varchar(300) COMMENT 'Name of the campaign',
  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign',
  spend double unsigned NOT NULL COMMENT 'Spend (Expense / 100)',
  conversions bigint(20) unsigned NOT NULL COMMENT 'Number of conversions',
  clicks bigint(20) unsigned NOT NULL COMMENT 'Number of clicks',
  installs bigint(20) unsigned NOT NULL COMMENT 'Number of installs',
  country_code varchar(2) NOT NULL COMMENT 'Country code in which the campaign took place',
  UNIQUE KEY idx1 (date, network, campaign_id, country_code)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='ironSource-related metrics. See https://developers.ironsrc.com/general/app-promoting/promotion-reporting-api/'
;

CREATE TABLE daily_stats_pinsight (
  date date NOT NULL COMMENT 'Date of the metric in UTC',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "pinsight")',
  cost double unsigned NOT NULL COMMENT 'Cost in dollars',
  conversions bigint(20) NOT NULL COMMENT 'Number of conversions',
  UNIQUE KEY idx1 (date, network)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='Pinsight-related metrics. See http://partners.pinsightmedia.com/stats/stats_api#stats'
;

CREATE TABLE daily_stats_facebook (
  date date NOT NULL COMMENT 'Date of the metric in UTC',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "facebook")',
  account_name varchar(300) NOT NULL COMMENT 'Name of the account',
  account_id bigint(20) unsigned NOT NULL COMMENT 'ID of the account',
  campaign_name varchar(300) NOT NULL COMMENT 'Name of the campaign',
  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign',
  adset_name varchar(300) NOT NULL COMMENT 'Name of the Adset',
  adset_id bigint(20) unsigned NOT NULL COMMENT 'ID of the Adset',
  ad_name varchar(300) NOT NULL COMMENT 'Name of the Ad',
  ad_id bigint(20) unsigned NOT NULL COMMENT 'ID of the Ad',
  frequency bigint(20) unsigned NOT NULL COMMENT 'Frequency of the Ad',
  impressions bigint(20) unsigned NOT NULL COMMENT 'Number of Impressions',
  clicks bigint(20) unsigned NOT NULL COMMENT 'Number of Clicks',
  reach bigint(20) unsigned NOT NULL COMMENT 'Reach of Ad',
  spend double unsigned NOT NULL COMMENT 'Spend'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='Facebook-related metrics. See https://developers.facebook.com/docs/marketing-apis/'
;


CREATE TABLE daily_stats_google (
  date date NOT NULL COMMENT 'Date of the metric in UTC',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "google")',
  campaign varchar(300) NOT NULL COMMENT 'Name of the Campaign',
  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign',
  impressions bigint(20) unsigned NOT NULL COMMENT 'Number of Impressions',
  clicks bigint(20) unsigned NOT NULL COMMENT 'Number of Clicks',
  spend double unsigned NOT NULL COMMENT 'Spend'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='Google-related metrics. See https://developers.google.com/adwords/api/docs/guides/start'
;

CREATE TABLE daily_stats_vungle (
  date date NOT NULL COMMENT 'Date of the metric in UTC',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "google")',
  campaign_name varchar(300) NOT NULL COMMENT 'Name of the Campaign',
  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign',
  impressions bigint(20) unsigned NOT NULL COMMENT 'Number of Impressions',
  clicks bigint(20) unsigned NOT NULL COMMENT 'Number of Clicks',
  spend double unsigned NOT NULL COMMENT 'Spend'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='Vungle-related metrics. See https://support.vungle.com/hc/en-us/articles/115003842687-Reporting-API-2-0-for-Advertisers'
;

CREATE TABLE daily_stats_twitter (
  date date NOT NULL COMMENT 'Date of the metric in UTC',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "twitter")',
  campaign_name varchar(300) NOT NULL COMMENT 'Name of the Campaign',
  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign',
  impressions bigint(20) unsigned NOT NULL COMMENT 'Number of Impressions',
  clicks bigint(20) unsigned NOT NULL COMMENT 'Number of Clicks',
  spend double unsigned NOT NULL COMMENT 'Spend'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='Twitter-related metrics. See https://developer.twitter.com/en/docs/ads/general/overview.html'
; 

CREATE TABLE daily_stats_growth_master (
  date date NOT NULL COMMENT 'Date of the metric in UTC',
  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "twitter")',
  account_name varchar(300) NOT NULL COMMENT 'Name of the account',
  account_id bigint(20) unsigned NOT NULL COMMENT 'ID of the account',
  campaign_name varchar(300) NOT NULL COMMENT 'Name of the Campaign',
  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign',
  adset_name varchar(300) NOT NULL COMMENT 'Name of the Adset',
  adset_id bigint(20) unsigned NOT NULL COMMENT 'ID of the Adset',
  ad_name varchar(300) NOT NULL COMMENT 'Name of the Ad',
  ad_id bigint(20) unsigned NOT NULL COMMENT 'ID of the Ad',
  frequency bigint(20) unsigned NOT NULL COMMENT 'Frequency of the Ad',
  impressions bigint(20) unsigned NOT NULL COMMENT 'Number of Impressions',
  clicks bigint(20) unsigned NOT NULL COMMENT 'Number of Clicks',
  spend double unsigned NOT NULL COMMENT 'Spend'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
ROW_FORMAT=DYNAMIC
COMMENT='Master table combining marketing stats from different networks'
; 
