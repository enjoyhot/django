from hello.models import *
def server_info_req(req):
	if req.is_ajax():
		ajax_type=req.POST['type']
		ip=req.POST['ip']
		if ajax_type=='1':					
			cimc_ip.objects(ip=ip).delete()
		else:
			if not cimc_ip.objects(ip=ip):
				newip=cimc_ip(ip=ip)
				newip.insert()
	return True
