import psutil

from network import get_ipv4

def collect_metrics(prev_net=None):
	cpu = psutil.cpu_percent(interval=None)
	mem = psutil.virtual_memory()
	disk = psutil.disk_usage("/")
	net = psutil.net_io_counters()

	net_delta = None
	if prev_net:
		net_delta = {
			"sent": net.bytes_sent - prev_net.bytes_sent,
			"recv": net.bytes_recv - prev_net.bytes_recv
	}

	return{
		"cpu": cpu,
		"mem": mem,
		"disk": disk,
		"net": net,
		"net_delta": net_delta,
		"ipv4": get_ipv4()
	}
