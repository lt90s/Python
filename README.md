# Python


```python
x = '0301002cc0a8016c00000000797500000000000000000000ffffff00000a000100000028c0a8016c00000000'

x = reduce(lambda x, y: x + struct.pack('B', int(y, 16)),  [a + b for a, b in zip(x[::2], x[1::2])], '')
print repr(x)
```


### explore flask

http://www.phperz.com/article/15/0831/153047.html


## create socket to recieve ospf packet

```python
import socket
import struct
IPPROTO_OSPF = 89
iface_ip = "a.b.c.d"
iface_name = "eth0"
ospf_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, IPPROTO_OSPF)

# join multicast group
mreq = struct.pack("4s4s", socket.inet_aton('224.0.0.5'), socket.inet_aton(iface_ip))
ospf_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# SO_BINDTODEVICE = 25, bind to interface
ospf_socket.setsockopt(socket.SOL_SOCKET, 25, iface_name)

# avoid recieving multicast packets sent from this socket, may not work
ospf_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

ospf_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
```
