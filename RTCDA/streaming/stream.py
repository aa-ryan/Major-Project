import subprocess
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import json

cluster = Cluster()
proc = subprocess.Popen(['kafka-console-consumer', '--bootstrap-server', 'localhost:9092', '--topic', 'cs', '--from-beginning'], stdout=subprocess.PIPE)
# kafka-console-consumer --bootstrap-server localhost:9092 --topic cs --from-beginning
i = 0
while True:
    line = proc.stdout.readline()
    if not line:
        break
    else:
        data_dict = json.loads(line)
        try:
            session = cluster.connect('wiki')
            print("Success")
        except:
            print("Fail")
            exit(0)