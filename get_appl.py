import meraki


dashboard = meraki.DashboardAPI(api_key = '')
networks = dashboard.organizations.getOrganizations()
print("\n")

for network in networks:
	print(f'{network["id"]} -- {network["name"]}\n')


usr_inp = input("Enter Network ID number: ")
a_network = dashboard.organizations.getOrganizationNetworks(usr_inp)

net_name = []
location_name = []

for i in a_network:
	print(f'{i["name"]}\t{i["id"]}')
	#print(f'{i["name"]}\t{i["id"]}\n\t{i["url"]} -- {i["productTypes"]} -- {i["timeZone"]} -- {i["tags"]} -- {i["isBoundToConfigTemplate"]}\n')
	net_name.append(i["id"])
	location_name.append(i["name"])


zip_list = zip(net_name, location_name)
app_list =[]


usr_inp1 = input("Enter Locations Network ID = L_xx... : ")
port_status = dashboard.appliance.getNetworkAppliancePorts(usr_inp1)
for i in port_status:
	app_list.append(i)

print("\n\n\n\n")
serial_list = []
dev = dashboard.networks.getNetworkDevices(usr_inp1)
for i in dev:
	#print(f'\n{i["name"]} -- {i["serial"]} -- {i["mac"]}')
	serial_list.append(i["serial"])



for ser in serial_list:
	try:
		response = dashboard.appliance.getDeviceApplianceUplinksSettings(ser)
		response1 = dashboard.devices.getDeviceClients(ser)
		# response = dashboard.networks.getNetworkTraffic(network_id, timespan=604800) # Network Traffic from 2592000 30days, 604800 7days
		# headers = response[0].keys()
	except meraki.APIError as e:
		# print(f'Meraki API error: {e}') print(f'status code = {e.status}') print(f'reason = {e.reason}') print(f'error = {e.message}\n\n\n')
		err_x = e
		continue
	except Exception as e:
		err_y = e
		continue
	
	wan1 = response["interfaces"]["wan1"]
	wan2 = response["interfaces"]["wan2"]
	wan1 = wan1["svis"]
	wan2 = wan2["svis"]
	wan1 = wan1["ipv4"]
	wan2 = wan2["ipv4"]
	
	for i, v in zip_list:
		if i == usr_inp1:
			matched_value = v
			break
	print(f'\n{matched_value}\nWAN1 Address = {wan1["address"]}')
	print(f'WAN1 Gateway = {wan1["gateway"]}\n')
	print(f'WAN2 Mode = {wan2['assignmentMode']}\n')

# print(app_list, "\n")
print(serial_list, "\n")

for i in response1:
	# search by vlan
  if i['vlan'] == 2:
		print(f'{i['description']} -- {i['ip']} -- {i['mac']}')


