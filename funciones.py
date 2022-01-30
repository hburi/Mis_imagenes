# -*- coding: utf-8 -*-
"""
Héctor Fernando Buri
Contenedor de funciones para el script reportes.py

"""
import re # Para evaluar IPs
import socket # Para scanear puertos
import paramiko # Para testear user y password
import os # Para verificar archivos existentes
from pythonping import ping # Para descartar inalcanzables


def ip_finder(text):
    
    'Machea un formato de IPv4, en caso que el campo en QB tenga más de un valor'
    
    ip = re.compile( r'[0-9]+(?:\.[0-9]+){3}')
    ip_list = ip.findall(text)
    return ip_list


def dot_format(cid):
    
    'Pasa el nombre a formato de punto, se usa para PoPs'
    
    new_text = ''

    for i in cid:
        new_letter = ''
        if i == '-':
            new_letter = '.'
        elif i == ' ' :
            pass
        else:
            new_letter = i
        new_text = new_text + new_letter
    return(new_text)


def dash_format(cid):
    
    'Pasa el nombre a formato de guión, se usa para servicios'
    
    new_text = ''

    for i in cid:
        new_letter = ''
        if i == '.':
            new_letter = '-'
        elif i == ' ' :
            pass
        else:
            new_letter = i
        new_text = new_text + new_letter
    return(new_text)


def port_selector(ip):
    
    'Escanea los puertos usuales y determina el que está abierto en el dispositivo, previamente determina alcanzabilidad'
    
    icmp_test = ping(ip).success()
    #print(icmp_test)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    if icmp_test == True:
        #print('ICMP OK')
        ports = [22,23,22022]
        for port in ports:
            try:
                s.connect((ip,port))
                return(port)
                print('Exito')
            except:
                print('sin PORT')
                pass
                
    else:
        return('no_value')
        print('ICMP failed')



def user_selector(ip,port,user, password,tacac_user,tacac_password):
    
    'Determina que user y password son admisibles en el equipo'
    
    if port == 'no_value':
        pass
    else:
        print(ip,port,user,'<===Usando USER SELECTOR')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, port, tacac_user, tacac_password)
            return(tacac_user, tacac_password)
            ssh.close()
        except:
            return(user,password)

def delete_last_line(xml_file):
    
    'Borra la última línea del archivo, se usa para borrar el cierre del XML, caso el archivo ya se haya creado y trabajado'
    
    if os.path.exists(xml_file):
        print('borrando linea final')
        file_read = open(xml_file,'r')
        lista_file = []
        
        for line in file_read:
            lista_file.append(line)
        try:
            lista_file.pop(-1)
        except:
            pass
        
        file_read.close()
        
        file_write = open(xml_file,'a')
        
        file_delete = open(xml_file,'w')
        #file_delete.write('<!--Nueva iteración-->' + '\n')
        file_delete.truncate(0)
        file_delete.close()
        
        for line in lista_file:
            file_write.write(line)
    
        file_write.close()
        
    else:
        #print('Haciendo nada')
        pass
        
        
    
def already_in_file(xml_file):
    
    'Crea una lista que contiene las IP que ya figuran o en el xml, o en el archivo de descartes'
    
    ip_in_file = [] 
    if os.path.exists(xml_file):
        file_read = open(xml_file,'r')
        
        for line in file_read:
            in_file = ip_finder(line)
            print(in_file, 'ya en archivo')
            if len(in_file) != 0:
                ip_in_file.append(in_file[0])
            else:
                pass
    if os.path.exists(xml_file+'_descartado'):
        file_read = open(xml_file+'_descartado','r')
        
        for line in file_read:
            in_file = ip_finder(line)
            print(in_file, 'ya en archivo descartado')
            if len(in_file) != 0:
                ip_in_file.append(in_file[0])
            else:
                pass
        
    return(ip_in_file)

