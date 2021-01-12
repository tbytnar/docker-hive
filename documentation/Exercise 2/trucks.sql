DROP TABLE IF EXISTS testing.trucks;

CREATE TABLE testing.trucks (
  `datetime` STRING,
  shipping_id STRING,
  shipping_name STRING,
  owner_id STRING,
  owner_name STRING,
  `status` STRING,
  `location` STRING
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
  "input.regex" = "([^ ]* [^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) (.*)",
  "output.format.string" = "%1$s %2$s %3$s %4$s %5$s %6$s %7$s"
)
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH "/tmp/trucks.txt" OVERWRITE INTO TABLE testing.trucks;