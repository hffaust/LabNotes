import sys
import os
from pymongo import MongoClient


def main(argv):
    print(argv)
    
    host = argv[0]
    port = argv[1]
    try:
        username = argv[2]
    except Exception as e:
        username = None
    try:
        password = argv[3]
    except Exception as e:
        password = None

    client = MongoClient(host, int(port), username=username, password=password)
    client.server_info()  # Basic Info
    
    # If you have admin access you can obtain more info
    admin = client.admin
    admin_info = admin.command("serverStatus")
    cursor = client.list_databases()

    for db in cursor:
        print(db)
        print(client[db["name"]].list_collection_names())
    #If admin access, you could dump the database



if __name__ =="__main__":
    main(sys.argv[1:])
