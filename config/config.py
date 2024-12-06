import socket

network_conf = dict(
    my_ip=socket.gethostbyname(socket.gethostname()),
    parent_ip='',
    child_ips=['']
)
