#!/usr/bin/env python
import os
import zipfile
import urllib2
from urllib2 import URLError
import time

def clear_webc_folder():
    folder = '/var/smb/ftp2/cameras/camera1'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e
    folder = '/var/smb/ftp2/cameras/camera2'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e            
    folder = '/var/smb/ftp2/cameras/temp'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e            

def clear_wc_folder(ordner):
    for the_file in os.listdir(ordner):
        file_path = os.path.join(ordner, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e          

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

def zip_webc_folder():
    zipf = zipfile.ZipFile('/var/smb/ftp2/cameras/temp/movement.zip', 'w')
    zipdir('/var/smb/ftp2/cameras/camera1', zipf)
    zipdir('/var/smb/ftp2/cameras/camera2', zipf)
    zipf.close()
   
def mail_webc_pics():
    folder1 = '/var/smb/ftp2/cameras/camera1'
    folder2 = '/var/smb/ftp2/cameras/camera2'
    filenp = "/var/smb/ftp2/cameras/temp/movement.zip"
    if not os.listdir(folder1) and not os.listdir(folder2) : return
    zip_webc_folder()
    exectext = "uuencode '"+filenp+"' 'movement.zip' | mailx -s 'Movement Detected' 'chrihuc@gmail.com'"
    os.system(exectext)
    clear_webc_folder()
    
def zip_wc_folder(ordner, datei):
    zipf = zipfile.ZipFile(datei, 'w')
    zipdir(ordner, zipf)
    zipf.close()
   
def send_wc_pix():
    ordner = '/mnt/array1/MIsc/recordings/'
    ordner_temp = "/mnt/array1/MIsc/rec_temp/"
    datei = "/mnt/array1/MIsc/rec_temp/recordings.zip"
    if not os.listdir(ordner) : return
    zip_wc_folder(ordner, datei)
    exectext = "uuencode '"+datei+"' 'recordings.zip' | mailx -s 'Aufnahmen von Eingangstuer' 'chrihuc@gmail.com'"
    os.system(exectext)
    exectext = "(uuencode '"+ordner+"web-cam-shot00.jpg' 'web-cam-shot00.jpg'; uuencode '"+ordner+"web-cam-shot01.jpg' 'web-cam-shot01.jpg'; uuencode '"+ordner+"web-cam-shot02.jpg' 'web-cam-shot02.jpg') | mailx -s 'Aufnahmen von Eingangstuer' 'chrihuc@gmail.com'"
    os.system(exectext)    
    clear_wc_folder(ordner)  
    clear_wc_folder(ordner_temp) 
    
def set_recording(camera = 1, recording = True):
    if camera == 1:
      teil1 = "http://192.168.192.30/set_ftp.cgi?cam_user=admin&cam_pwd=&svr=192.168.192.10&port=21&user=camera1&pwd=camera1&dir=/var/smb/ftp2/cameras/camera1"
    else:
      teil1 = "http://192.168.192.31/set_ftp.cgi?cam_user=admin&cam_pwd=&svr=192.168.192.10&port=21&user=camera2&pwd=camera2&dir=/var/smb/ftp2/cameras/camera2"
    if recording:
      teil2 = "&mode=0&upload_interval=1&filename=&numberoffiles=0"
    else:
      teil2 = "&mode=0&upload_interval=0&filename=&numberoffiles=0"
    body = teil1 + teil2
    try:
        f = urllib2.urlopen(body)
    except URLError as e:
        pass   
    #http://192.168.192.30/set_ftp.cgi?user=admin&pwd=&svr=192.168.192.10&port=21&user=camera1&pwd=camera1&dir=/var/smb/ftp2/cameras/camera1&mode=0&upload_interval=1&filename=&numberoffiles=0 
    
def send_to_cam(command):
    try:
        f = urllib2.urlopen(command)
        return "ok"
    except URLError as e:
        return "not ok"
    
def set_position():
    up="http://192.168.192.31/decoder_control.cgi?user=admin&pwd=&command=0&onestep=1"
    set_vga="http://192.168.192.31/camera_control.cgi?user=admin&pwd=&param=0&value=32"
    move_left="http://192.168.192.31/decoder_control.cgi?user=admin&pwd=&command=4&onestep=1"
    center="http://192.168.192.31/decoder_control.cgi?user=admin&pwd=&command=25"
    print send_to_cam(set_vga)
    time.sleep(0)
    #print send_to_cam(center)
    time.sleep(1)
    for i in range(6):
        send_to_cam(move_left)
        time.sleep(0.5)
    time.sleep(1)
    send_to_cam(up)

if __name__ == '__main__':
    send_wc_pix()
    #set_recording(camera = 2, recording = True) 
    #time.sleep(5)
    #set_recording(camera = 2, recording = False) 