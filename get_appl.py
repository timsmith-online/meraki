import meraki



dashboard = meraki.DashboardAPI(api_key = '')
networks = dashboard.organizations.getOrganizations()
print("\n")



def try_fun(command):
	try:
		resp = command
	except meraki.APIError as e:
		print(f'Meraki API error: {e}')
		print(f'status code = {e.status}')
		print(f'reason = {e.reason}')
		print(f'error = {e.message}')
	except Exception as e:
		print(f'ERR: {e}')
	return resp




for network in networks:
	print(f'{network["id"]} -- {network["name"]}\n')



usr_inp = input("Enter Network ID number: ")
a_network = dashboard.organizations.getOrganizationNetworks(usr_inp)
print("\n\n\n\n")



net_name = []
location_name = []
for i in a_network:
	print(f'{i["name"]}\t{i["id"]}')
	net_name.append(i["id"])
	location_name.append(i["name"])



zip_list = zip(net_name, location_name)
app_list =[]
usr_inp1 = input("Enter Locations Network ID (L_xx...): ")
port_status = dashboard.appliance.getNetworkAppliancePorts(usr_inp1)
for i in port_status:
	app_list.append(i)
print("\n\n\n\n")



serial_list = []
model_list = []
dev = dashboard.networks.getNetworkDevices(usr_inp1)
for i in dev:
	print(f'\t{i["model"]} -- {i["serial"]} -- {i["name"]}')
	serial_list.append(i["serial"])
	model_list.append(i["model"])
print("\n")



sm_list = zip(serial_list, model_list)
for sm in sm_list:
	# Switches
	if sm[1] == "MS355-48X":
		switch_port_status=try_fun(command=dashboard.switch.getDeviceSwitchPorts(sm[0]))
		for i in switch_port_status:
			print(f'\tport={i["portId"]} -- vlan={i["vlan"]} -- {i["name"]}')
		print("\n")
	# Firewalls
	elif sm[1] == "MX84":
		wan_port_status=try_fun(command=dashboard.appliance.getDeviceApplianceUplinksSettings(sm[0]))
		wan1 = wan_port_status["interfaces"]["wan1"]
		wan2 = wan_port_status["interfaces"]["wan2"]
		wan1 = wan1["svis"]["ipv4"]
		wan2 = wan2["svis"]["ipv4"]
		print(f'\t{wan1}\n')
		print(f'\t{wan2}\n')
	# APs
	else:
		continue
