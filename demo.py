# coding:utf-8
'''
在报文送往用户空间进程处理之前，对报文进行进一步处理，这个例子中只打印报文16进制信息
iptables -I INPUT -d 189.48.54.93/32 -p gre -j NFQUEUE --queue-num 1
'''

import socket
import libevent
from netfilterqueue import NetfilterQueue as NFQ


'''
Get packet from NetfilterQueue and give it to other
modules to handle
'''
class Packet_Engin(object):
    def __init__(self, handler, queue=1):
        self.evt_base = libevent.Base()
        self.setup_NFQ(handler, queue)
        self.nfq_evt = self.add_persist_read_event(
                            self.nfq_fd, self.nfq_event_handler, self)

    def __del__(self):
        self.nfq_socket.close()
        self.nfq.unbind()

    def setup_NFQ(self, handler, queue):
        self.nfq = NFQ(queue)
        self.nfq.bind(queue, handler)
        self.nfq_fd = self.nfq.get_fd()
        self.nfq_socket = socket.fromfd(self.nfq_fd, \
                        socket.AF_UNIX, socket.SOCK_STREAM)
        self.nfq_socket.setblocking(False)

    # returned evt must be kept live until you are done with it
    def add_event(self, fd, flag, cb, cb_data, timeout=0):
        evt = libevent.Event(self.evt_base, fd, flag, cb, cb_data)
        evt.add(timeout)
        return evt

    def add_persist_read_event(self, fd, cb, cb_data, timeout=0):
        return self.add_event(fd, libevent.EV_READ | libevent.EV_PERSIST,
                                    cb, cb_data, timeout)

    def add_persist_timer(self, cb, cb_data, timeout):
        return self.add_event(-1, libevent.EV_TIMEOUT | libevent.EV_PERSIST,
                                    cb, cb_data, timeout)

    @staticmethod
    def nfq_event_handler(evt, fd, what, self):
        self.nfq.run_socket(self.nfq_socket)



    def start(self):
        self.evt_base.loop()


if __name__ == '__main__':
    def show_pkt(pkt):
        from scapy.layers import inet, l2
        from scapy.utils import hexdump
        payload = pkt.get_payload()
        ip = inet.IP(payload)
        print '%s to %s' %(ip.src, ip.dst)
        hexdump(ip)
#pkt.drop()
        pkt.accept()

    def timeout_handler(evt, fd, what, self):
        print 'timeout'

    pe = Packet_Engin(show_pkt, 1)
    #evt_timeout = pe.add_persist_timer(timeout_handler, None, 5)
    pe.start()
