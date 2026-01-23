import psutil
import socket

def get_ipv4():
	interfaces = psutil.net_if_addrs()

	for iface, addrs in interfaces.items():
		for addr in addrs:
			if addr.family != socket.AF_INET:
				continue

			if addr.address == "127.0.0.1":
				continue

			return{
				"interface": iface,
				"ip": addr.address
			}

	return None


