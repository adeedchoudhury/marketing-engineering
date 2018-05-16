+CREATE TABLE daily_stats_facebook (
+  date date NOT NULL COMMENT 'Date of the metric in UTC',
+  network varchar(100) NOT NULL COMMENT 'Name of the network (e.g. "facebook")',
+  account_name varchar(300) NOT NULL COMMENT 'Name of the account'
+  account_id bigint(20) unsigned NOT NULL COMMENT 'ID of the account'
+  campaign_name varchar(300) NOT NULL COMMENT 'Name of the campaign'
+  campaign_id bigint(20) unsigned NOT NULL COMMENT 'ID of the campaign'
+  adset_name varchar(300) NOT NULL COMMENT 'Name of the Adset'
+  adset_id bigint(20) unsigned NOT NULL 'ID of the Adset'
+  ad_name varchar(300) NOT NULL COMMENT 'Name of the Ad'
+  ad_id bigint(20) unsigned NOT NULL 'ID of the Ad'
+  frequency bigint(20) unsigned NOT NULL 'Frequency of the Ad'
+  impressions bigint(20) unsigned NOT NULL 'Number of Impressions'
+  clicks bigint(20) unsigned NOT NULL 'Number of Clicks'
+  reach bigint(20) unsigned NOT NULL 'Reach of Ad'
+  spend double unsigned NOT NULL COMMENT 'Spend'
+)
+ENGINE=InnoDB
+DEFAULT CHARSET=utf8mb4
+ROW_FORMAT=DYNAMIC
+COMMENT='Facebook-related metrics. See https://developers.facebook.com/docs/marketing-apis/'
+;


