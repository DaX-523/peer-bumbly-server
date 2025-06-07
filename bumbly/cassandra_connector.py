from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def get_session():
    cluster = Cluster(['172.19.0.2'])  # Or Docker IP
    session = cluster.connect('bumbly')
    return session
