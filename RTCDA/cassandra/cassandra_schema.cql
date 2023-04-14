CREATE KEYSPACE wiki WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};

USE wiki;
 
CREATE TABLE batch_source (source text, topic text, count int, PRIMARY KEY(source, count)) with CLUSTERING ORDER BY (count DESC);

CREATE TABLE batch_topic (source text, topic text, count int, PRIMARY KEY(topic, count)) with CLUSTERING ORDER BY (count DESC);

CREATE TABLE pagerank (topic text, rank double, date date, PRIMARY KEY(date, rank)) WITH CLUSTERING ORDER BY (rank DESC);

CREATE TABLE realtime (source text, count int, timestamp timestamp, PRIMARY KEY(source, timestamp, count)) WITH CLUSTERING ORDER BY (timestamp DESC, count DESC);

