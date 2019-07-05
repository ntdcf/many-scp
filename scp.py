# -*- coding:utf-8 -*-
import os
import paramiko
import configparser
import sys

conf_path = "./conf/"

def get_hosts_info():
    config = configparser.RawConfigParser()
    config.read(conf_path + 'upload.cfg')

    username = config.get('host', 'username')
    password = config.get('host', 'password')
    hosts = config.get('host', 'hosts')
    port = config.get('host', 'port')

    hosts_arr = hosts.split(',')
    return username,password,hosts_arr,port


def scp_put(local_file, remote_file, fname):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    user,passwd,hosts,port = get_hosts_info()
    
    for host in hosts:
        ssh_client.connect(host, port, username=user, password=passwd)

        home_path = '/home/' + user
        
        # 传到home
        sftp = paramiko.SFTPClient.from_transport(ssh_client.get_transport())
        sftp = ssh_client.open_sftp()
        sftp.put(local_file, os.path.join(home_path, fname))

        # 移动到指定文件夹
        stdin, stdout, stderr = ssh_client.exec_command('sudo mv '+home_path+'/'+fname + ' ' + remote_file)
        stdin.write(passwd+'\n')
        stdin.flush()
        stdout.read()
        print('success ' + host)
    

if __name__ == "__main__":
    config = configparser.RawConfigParser()
    config.read(conf_path + 'upload.cfg')
    
    if len(sys.argv) <= 1 :
        print('argv project names')
    else:
        for i in range(1, len(sys.argv)):
            config_tag = sys.argv[i]
            local_file = config.get(config_tag, 'local_file')
            remote_file_path = config.get(config_tag, 'remote_file_path')
            file_name = config.get(config_tag, 'file_name')
            
            scp_put(local_file, remote_file_path, file_name)
            print('project ' + sys.argv[i] + ' is ending')