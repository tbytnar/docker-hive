DROP TABLE IF EXISTS testing.drivers;

CREATE EXTERNAL TABLE testing.drivers
(
    id INT,
    firstname STRING,
    lastname STRING,
    startdate STRING,
    rate INT,
    location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH "/tmp/drivers.csv" OVERWRITE INTO TABLE testing.drivers;