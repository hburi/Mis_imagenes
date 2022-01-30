
#import json
import requests
from funciones import dot_format, ip_finder, dash_format



tac_user = 'tacacs_user'
tac_pass = 'tacacs_password'



headers = {
  	'QB-Realm-Hostname': 'ignetworks.quickbase.com',
	'User-Agent': 'FileService_Integration_V2.1',
	'Authorization': 'QB-USER-TOKEN b48wfv_w4i_0_dqwgkkvd65kd59b45w34icmbyqrd'
}
params = {
  	'tableId': 'bjj6j8a3g',
	'skip': '0',
	'top': '10000'
}
r = requests.post(
'https://api.quickbase.com/v1/reports/1000065/run', 
params = params, 
headers = headers
)

'''
{'177': {'value': 'Supermicro'}, '207': {'value': ''}, '25': {'value': '172.20.2.20'}, '26': {'value': False}, '27': {'value': ''}, '47': {'value': 'SAO3-SRV2'}}
'''

#print(json.dumps(r.json(),indent=4))

#print(type(r.json()))

diccionario = r.json()




data = diccionario.get('data')
fields = diccionario.get('fields')
metadata = diccionario.get('metadata')

#print(data)

superlista = []


for dic in data:
    lista = []
    
    lista.append(dic.get('177').get('value')) #brand
    lista.append(dic.get('25').get('value')) #IP
    lista.append(dic.get('26').get('value')) #TACACS
    lista.append(dic.get('27').get('value')) #user
    lista.append(dic.get('28').get('value')) #password
    lista.append(dic.get('47').get('value')) #name
    
    superlista.append(lista)
    
brands = []    
devices = {}

for i in range(0, len(superlista)):
    if superlista[i][0] in brands:
        pass
    else:
        brands.append(superlista[i][0])
        

for brand in brands:
    devices[brand] = []
    
for i in range(0, len(superlista)):
    list = []
    list.append(superlista[i][1])
    list.append(superlista[i][2])
    list.append(superlista[i][3])
    list.append(superlista[i][4])
    list.append(superlista[i][5])
    devices[superlista[i][0]].append(list)
    
 
session_delete = open('full_devices.xml','w').close()    
    
session_header = open('full_devices.xml','a')
session_header.writelines(['<?xml version="1.0" encoding="utf-8"?>\n',
                       '<ArrayOfSessionData xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'])
session_header.close()

#<SessionData SessionId="BUE1/BUE1.ASW1" SessionName="BUE1.ASW1" ImageKey="computer" 
#    Host="172.20.4.2" Port="22" Proto="SSH" PuttySession="Default Settings" Username="hburi" 
#ExtraArgs="-pw  tmqKwf5k" SPSLFileName="" />

#['172.23.31.153', False, 'noc', 'UndvlgRp', ' TXB-5577-A004-PontaA-PE01'] 

#['172.20.1.7', False, 'admin', 'versa123', 'MIA1-HUB1']
        
session_data = open('full_devices.xml','a')

for brand in brands:
    if brand == 'Mikrotik':
        port = '22022'
    else:
        port = '22'
    
    list_brand = devices[brand]
    
    for host in list_brand:
        
        ip = ip_finder(host[0])[0]
        name = dot_format(host[4])
        name_list = dot_format(host[4]).split('.')
        
        if len(name_list) == 2:
            folder_1 = 'PoP'
            name = dash_format(name)
        elif len(name_list) >= 2 and name_list[1].isnumeric() == True:
            folder_1 = 'Clients'
        else:
            folder_1 = 'Others'
        
        if brand == 'Mikrotik':
            user = host[2]
            password = host[3]
        else:
            if  host[1] == True:
                #print(host)
                user = tac_user
                password = tac_pass
            else:
                user = host[2]
                password = host[3]
        
        #print(port, ip, name, folder_1, user, password)
    
        line = '  <SessionData SessionId="' + folder_1 + '/' + name_list[0] + '/' + name  + ' (' + brand + ')' + '" SessionName="' + name +'" ImageKey="computer" Host="' + ip + '" Port="' + port + '" Proto="SSH" PuttySession="Default Settings" Username="' + user + '" ExtraArgs="-pw  ' + password + '" SPSLFileName="" />'
        
        #if ('&' in line) or (host[0] == '') or (host[2] == '') or (host[3] == '') or (host[4] == '') or (folder_1 == 'Others'):
        
        if ('&' in line) or (host[0] == '') or (host[4] == '') or (folder_1 == 'Others'):
            pass
        else:
            session_data.write(line + '\n')
        
        
        
session_data.write('</ArrayOfSessionData>')        
session_data.close()
        
        
#print(devices)