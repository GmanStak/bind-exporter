导入dns. 解析器、json、prometheus_client
从prometheus_client导入仪表
来自prometheus_client。core导入CollectorRegistry
从烧瓶导入响应，烧瓶
从gevent导入pywsgi
从参数导入get_args

应用程序=烧瓶（ __name__ ）

REGISTRY = CollectorRegistry  ( auto_describe= False )
domain_status = Gauge ( "domain_status" , "DNS 服务器域名状态。" , [ 'server_ip' , 'domain' , 'hostname' ] ,registry=REGISTRY )

def  get_domain_stats (服务器、端口、域、dns_type= "A" ) :
    服务器=服务器
    端口=端口
    dns_q = dns.dns. 留言。make_query （域，dns_type ）
    尝试：
        a = 域名。查询。udp ( dns_q、服务器、端口=端口、超时= 0.1、raise_on_truncation= False )
        返回 真
    除外：
        返回 错误

参数 = get_args ( )
配置路径=参数。配置

def  read_config ( config_path ) :
    打开 （ config_path ）作为json_file： 
        配置=json. 加载（ json_file ）
    返回配置

@ app.route ( '/' )
定义 索引( ) :
    返回 “<h1>自定义导出器</h1><br><a href='metrics'>指标</a>”

@ app.route ( '/metrics' )
定义 指标( ) :
    配置=读取配置（配置路径）
    # 全局().更新(配置)
    对于配置中的config_list ：
        dns_list = config_list [ '域' ]
        服务器 = config_list [ 'server_ip' ]
        端口 = config_list [ '端口' ]
        对于dns_list中的dns_name ：
            结果 = get_domain_stats (服务器、端口、dns_name )
            如果结果：
                域状态。标签（ server_ip = config_list [ 'server_ip' ]，domain = dns_name，hostname = config_list [ 'hostname' ] ）。套装( 1 )
            其他：
                域状态。标签（ server_ip = config_list [  'server_ip'  ]，domain = dns_name，hostname = config_list [  'hostname'  ]  ）。集(  0  )
    返回响应( prometheus_client.generate_latest ( REGISTRY ) , mimetype= " text /plain " )  
如果__name__ == "__main__"：
    # app.run(主机='0.0.0.0',端口=9119,线程=True)
    服务器 = pywsgi. WSGIServer（（'0.0.0.0' ，9119 ），应用程序）
    服务器。永远服务（）
