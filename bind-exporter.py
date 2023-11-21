import dns.resolver, json, prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from gevent import pywsgi
from arguments import get_args

app = Flask(__name__)

REGISTRY = CollectorRegistry(auto_describe=False)
domain_status = Gauge("domain_status","DNS server Domain Name status.",['server_ip','domain','hostname'],registry=REGISTRY)

def get_domain_stats(server, port, domain, dns_type="A"):
    server = server
    port = port
    dns_q = dns.message.make_query(domain, dns_type)
    try:
        a = dns.query.udp(dns_q, server, port=port, timeout=0.1, raise_on_truncation=False)
        return True
    except:
        return False

args = get_args()
config_path = args.config

def read_config(config_path):
    with open(config_path) as json_file:
        config = json.load(json_file)
    return config

@app.route('/')
def index():
    return "<h1>Customized Exporter</h1><br> <a href='metrics'>Metrics</a>"

@app.route('/metrics')
def metrics():
    domain_status.clear()
    config = read_config(config_path)
    # globals().update(config)
    for config_list in config:
        dns_list = config_list['domain']
        server = config_list['server_ip']
        dns_port = config_list['port']
        for dns_name in dns_list:
            result = get_domain_stats(server, dns_port, dns_name)
            if result:
                domain_status.labels(server_ip=config_list['server_ip'], domain=dns_name, hostname=config_list['hostname']).set(1)
            else:
                domain_status.labels(server_ip=config_list['server_ip'], domain=dns_name, hostname=config_list['hostname']).set(0)
    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")
if __name__ == "__main__":
    host = args.ipaddress
    port = args.port
    # app.run(host='0.0.0.0',port=9119,threaded=True)
    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()
