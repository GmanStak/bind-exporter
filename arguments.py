import argparse

def get_args():
    parser = argparse.ArgumentParser(description='bind export options!')
    parser.add_argument("-a","--ipaddress",type=str,default='localhost')
    parser.add_argument("-p","--port",type=int,default=9119)
    parser.add_argument("-c","--config",type=str,default="./conf/domain.json")
    args = parser.parse_args()
    return args
