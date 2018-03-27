import os
path = os.path.dirname(__file__)
path = os.path.join(path, 'database.db')


DB_URI = 'sqlite:///' + path


RE_RULE = {
    "http://www.kuaidaili.com/free/": "IP\">([\d\.]+)</td>\s*<td data-title=\"PORT\">(\d+)</td>",
    "http://www.66ip.cn/nmtq.php?getnum=512&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip": "([\d\.]+):(\d+)",
    "http://www.xicidaili.com/nn/": "<td>([\d\.]+)</td>\s*<td>(\d+)</td>",
    "http://www.ip3366.net/free/": "<td>([\d\.]+)</td>\s*<td>(\d+)</td>",
    "http://www.mimiip.com/": "<tr>\s+<td>([\d\.]+)</td>\s+<td>(\d+)</td>",
    "http://www.data5u.com/free/index.shtml": "<li>([\d\.]+)</li></span>\s+<span style=\"width: 100px;\"><li class=\".*\">(\d+)</li>",
    "http://www.ip181.com/": "<tr.*>\s+<td>([\d\.]+)</td>\s+<td>([\d]+)</td>",
    "http://www.kxdaili.com/": "<tr.*>\s+<td>([\d\.]+)</td>\s+<td>([\d]+)</td>",
}


VERIFY_URL = 'http://www.baidu.com'
VERIFY_TIMEOUT = 5


MAX_THREAD = 1024
