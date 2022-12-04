## Steps to Operate

- Installing Kafka and Zookeeper
	* $ brew cask install java
	* $ brew install kafka
- Start Zookeeper
	* zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
- Start Kafka Server
	* kafka-server-start /usr/local/etc/kafka/server.properties
- Create topic
	* kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic topic-name
	> Prefer clickstream as in producer code
- Run producer 
	* python producer.py path_to_preprocessed_data bootstrap_server

- For consumer
	* kafka-console-consumer --bootstrap-server localhost:9092 --topic topic-name --from-beginning
	> Manual Consumer from commandline
	> Python Script (to be done)

- list topics
	* kafka-topics --list --bootstrap-server 192.168.1.21:9092
