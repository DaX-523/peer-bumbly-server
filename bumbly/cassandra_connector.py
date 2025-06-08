from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def get_session():
    try:
        cluster = Cluster(['172.19.0.2'])  
        session = cluster.connect('bumbly')
        return session
    except Exception as error:
        print(error)
        return None
