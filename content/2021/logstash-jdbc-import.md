Title: Logstash import data from jdbc
Status: published
Date: 2021-08-06 18:00
Modified: 2021-08-06 18:00
Category: Java
Tags: java, elasticsearch
Slug: logstash-import-data-from-jdbc
Authors: Martin
Summary: logstash 从数据库导入数据


## 一次性导入

logstash 是基于jruby的，也可以使用jdbc，从数据库中导入数据也很方便。

下面是个例子，而且加入了IP地址到地理位置的转换：

```logstash
input {
 jdbc {
       jdbc_validate_connection => true
       jdbc_connection_string => "jdbc:oracle:thin:@192.168.100.1:1521:orcl"
       jdbc_user => "read"
       jdbc_password => "readonly"
       jdbc_driver_library => "D:\ojdbc6.jar"
       jdbc_driver_class => "Java::oracle.jdbc.driver.OracleDriver"
       jdbc_paging_enabled => true
       statement => "select t.log_id, t.log_time, t.client_ip, t.user_agent, t.browser, t.browser_type, t.browser_major_version, t.device_type, t.platform, t.platform_version from sys_log t 
       where EXTRACT(year from t.log_time) > 2020"
       lowercase_column_names => false
   }
}

filter {
  mutate {
    rename => { "LOG_ID" => "logId"}
    rename => { "LOG_TIME" => "@timestamp"}
    rename => { "CLIENT_IP" => "ip"}
    rename => { "USER_AGENT" => "ua"}
    rename => { "BROWSER" => "browser"}
    rename => { "BROWSER_TYPE" => "browserType"}
    rename => { "BROWSER_MAJOR_VERSION" => "browserMajorVersion"}
	  rename => { "DEVICE_TYPE" => "deviceType"}
	  rename => { "PLATFORM" => "platform"}
	  rename => { "PLATFORM_VERSION" => "platformVersion"}
  }
  geoip {
    source => "ip"
    database => "D:\logstash-7.3.1\GeoLite2-City_20210804\GeoLite2-City.mmdb"
  }
}

output {
  stdout { codec => rubydebug }

if "_jsonparsefailure" not in [tags] {
  elasticsearch {
    hosts => ["192.168.100.2:9200"]
    index => "sys-log-2021"
    }
  }
}
```

## 持续导入

如果日志是持续性导入，可以 track 上次导入的进度，下次在此基础上做增量导入。

```logstash
input {
 jdbc {
       jdbc_validate_connection => true
       jdbc_connection_string => "jdbc:oracle:thin:@192.168.100.1:1521:orcl"
       jdbc_user => "read"
       jdbc_password => "readonly"
       jdbc_driver_library => "D:\ojdbc6.jar"
       jdbc_driver_class => "Java::oracle.jdbc.driver.OracleDriver"
       jdbc_paging_enabled => true
       statement => "select t.log_id, t.log_time, t.client_ip, t.user_agent, t.browser, t.browser_type, t.browser_major_version, t.device_type, t.platform, t.platform_version from sys_log t 
       where EXTRACT(year from t.log_time) > 2020 and t.log_id > :sql_last_value order by t.log_id asc"
       lowercase_column_names => false

       # tracking
       parameters => { "sql_last_value" => 0 }
       use_column_value => true
       tracking_column => "LOG_ID"
       tracking_column_type => "numeric"
       # 每分钟执行一次
       schedule => "0 * * * * *"
   }
}

filter {
  mutate {
    rename => { "LOG_ID" => "logId"}
    rename => { "LOG_TIME" => "@timestamp"}
    rename => { "CLIENT_IP" => "ip"}
    rename => { "USER_AGENT" => "ua"}
    rename => { "BROWSER" => "browser"}
    rename => { "BROWSER_TYPE" => "browserType"}
    rename => { "BROWSER_MAJOR_VERSION" => "browserMajorVersion"}
	  rename => { "DEVICE_TYPE" => "deviceType"}
	  rename => { "PLATFORM" => "platform"}
	  rename => { "PLATFORM_VERSION" => "platformVersion"}
  }
  geoip {
    source => "ip"
    database => "D:\logstash-7.3.1\GeoLite2-City_20210804\GeoLite2-City.mmdb"
  }
}

output {
  stdout { codec => rubydebug }

if "_jsonparsefailure" not in [tags] {
  elasticsearch {
    hosts => ["192.168.100.2:9200"]
    index => "sys-log-2021"
    }
  }
}
```

记录上次 sql_last_value 的临时文件是 last_run_metadata_path，默认值是 "$HOME/.logstash_jdbc_last_run"


