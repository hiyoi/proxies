# coding: utf-8
import requests
import re
import random
from fake_useragent import UserAgent
import config
from log import logger
from db import Proxy
from db import eng
from sqlalchemy.orm import sessionmaker
from threading import Thread
from queue import Queue
ua = UserAgent()

DBSession = sessionmaker(eng)

session = DBSession()
queue = Queue()

delete_q = []


def get_useragent():
    return ua.chrome


def fetch(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ru;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': get_useragent()
    }
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.content
    except Exception as e:
        raise e


def get_address():
    try:
        for url in config.RE_RULE.keys():
            rule = config.RE_RULE.get(url)
            content = fetch(url)
            for item in re.findall(rule, content):
                addr = item[0] + ':' + item[1]
                proxy = Proxy(addr=addr)
                session.add(proxy)
                session.commit()
                logger.debug(item[0] + ':' + item[1])
    except Exception:
        session.rollback()
    finally:
        session.close()


def verify():
    while True:
        if queue.empty():
            return
        proxs = queue.get()
        proxies = {
            'http': proxs.address
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, compress',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ru;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': get_useragent()
        }
        try:
            resp = requests.get(config.VERIFY_URL,
                                proxies=proxies, headers=headers, timeout=config.VERIFY_TIMEOUT)
            if resp.status_code is 200:
                logger.debug(proxs.address + ' is useful')
            else:
                delete_q.append(proxs)
        except Exception as e:
            logger.debug(e)
            delete_q.append(proxs)


def verify_address():
    proxs = session.query(Proxy).all()
    for prox in proxs:
        queue.put(prox)
    thread_list = []
    for i in range(0, config.MAX_THREAD):
        t = Thread(target=verify)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    for prox in delete_q:
        try:
            session.delete(prox)
            session.commit()
            logger.debug('delete id' + str(prox.id) + ' ' + prox.address)
        except Exception as e:
            logger.debug(e)
        finally:
            session.close()


def get():
    pros = session.query(Proxy).all()
    pro = random.choice(pros)
    return pro.address
