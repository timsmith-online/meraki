import meraki
import csv
import time
import pandas as pd
import xlsxwriter

API_KEY = ""
dashboard = meraki.DashboardAPI(API_KEY)


net_name = []
location_name = []
csv_files = []


for i in range(len(net_name)):
	print(f'\n\n{net_name[i]} <------------------------------Getting Traffic Analytics----------------------------\n\n')
	network_id = net_name[i]
	try:
		response = dashboard.networks.getNetworkTraffic(network_id, timespan=604800) # 604800 7days, 2592000 30days
		headers = response[0].keys()
	except meraki.APIError as e:
		print(f'Meraki API error: {e}')
		print(f'status code = {e.status}')
		print(f'reason = {e.reason}')
		print(f'error = {e.message}')
		continue
	except Exception as e:
		print(f'ERR: {e}')
		continue
	time.sleep(1)
	csv_name = location_name[i] + ".csv"
	with open(csv_name, 'w', newline='') as file:
		writer = csv.DictWriter(file, fieldnames=headers)
		writer.writeheader()
		writer.writerows(response)
		print(f'\n{csv_name} <----------------------------------------Exported\n')
		csv_files.append(csv_name)


print("COMPLETED, now merging...")
time.sleep(5)


with pd.ExcelWriter('combined_excel.xlsx', engine='xlsxwriter') as writer:
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df.to_excel(writer, sheet_name=csv_file, index=False)
        print(csv_file)
