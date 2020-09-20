# coding: utf8

# optparse 库解析命令行参数
import optparse
import sys
from socket import *
from threading import *

screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        #screenLock.acquire()
        print('[+] %d/tcp open' % tgtPort)
        print('[+] ' + str(results))
    except:
        #screenLock.acquire()
        print('[-] %d/tcp closed' % tgtPort)
    finally:
        #screenLock.acquire()
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan Results for: ' + tgtIP)

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():

    # 添加两个参数 -H 和 -P，分别指定目标主机的 IP 地址和端口
    parser = optparse.OptionParser('usage %prog ' +\
                                   '-H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string',\
                      help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string',\
                      help='specify target port[s] separated by comma')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')

    # tgtHost 与 tgtPort 不能为空
    if (tgtHost == None) | (tgtPorts[0] == None):
        print('[-] You must specify a target host and port[s].')
        sys.exit(0)

    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()