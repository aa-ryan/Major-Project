from kafka import KafkaProducer
import sys
import time
import csv
import json
from datetime import datetime
import pandas as pd
import numpy as np


class Producer(object):

    def run(self, data_path, bootstrap_servers):
        try:
            producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
            df = pd.read_csv(data_path)
            for msg_cnt in range(3000000):
                i = np.random.randint(1000)
                data = df.iloc[i:i+1]
                message_info = {'prev_title': df.at[i, 'prev_title'],
                                'curr_title': df.at[i, 'curr_title'],
                                'type': df.at[i, 'type'],
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }
                message_info = json.dumps(message_info)
                print (message_info)
                producer.send('cs', message_info.encode('utf-8'))
                # time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            print("BYE")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: producer <data_path> <bootstrap_servers>")
        exit(-1)
    prod = Producer()
    prod.run(sys.argv[1], sys.argv[2])
