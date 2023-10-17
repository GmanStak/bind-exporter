# 基于Flask的域名检测
# 程序说明
利用dns.resolver，对dns服务器+dns端口+域名进行解析
# 启动参数说明
"-a","--ipaddress"，指定服务启动的IP地址，默认：localhost
"-p","--port"，指定服务启动的端口，默认：9119
"-c","--config"，指定配置文件路径，默认：./conf/domain.json、
# 配置文件说明
配置文件为json文件，需要指定：server_ip：dns服务器的地址（类型：str），hostname：dns服务器的主机名（类型：str）port：dns服务器的端口（类型：int），domain：域名列表（类型：list）
