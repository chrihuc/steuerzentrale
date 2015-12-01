#!/usr/bin/env python

import constants

import urllib, urllib2
import sys
import time
import mad
#from szenen import set_szene, sonos_set_szene
from time import localtime,strftime
from datetime import datetime
import subprocess

def main():
    lt = localtime()
    stunde = int(strftime("%H", lt))
    minute = int(strftime("%M", lt))    
    sonos_durchsage("Es ist " + str(stunde) + " Uhr und " + str(minute) + " Minuten.")

def downloadAudioFile(text):
    if constants.tts:
        subprocess.call(["espeak", "-w/mnt/array1/Musik/texttosonos.wav", "-a140", "-vmb-de6", "-p40", "-g0", "-s110", text])# a:volume p:pitch g:gaps s:words per minute
        subprocess.call(["ffmpeg", "-v" , "-8", "-i","/mnt/array1/Musik/texttosonos.wav", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3" ,"-y", "/mnt/array1/Musik/texttosonos.mp3"])
        mf =  mad.MadFile("/mnt/array1/Musik/texttosonos.mp3")
        return (mf.total_time()/1000)
    else:
        return 0
    
def downloadAudioFile_old(text):
    '''
        Donwloads a MP3 from Google Translatea mp3 based on a text and a 
        language code.
    '''
    filee = open("/mnt/array1/Musik/texttosonos.mp3", 'w')
    query_params = {"tl": "de", "q": text, "total": len(text)}
    url = "http://translate.google.com/translate_tts?ie=UTF-8" + "&" + unicode_urlencode(query_params)
    #url = "http://translate.google.com/translate_a/t?client=t&hl=en" + "&" + unicode_urlencode(query_params)
    #print url
    headers = {"Host":"translate.google.com", "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36"} #{"Host":"translate.google.com", "User-Agent":"Mozilla/5.10", "rel":"noreferrer"}
    req = urllib2.Request(url, '', headers)
    sys.stdout.write('.')
    sys.stdout.flush()
    try:
        response = urllib2.urlopen(req)
        print response
        filee.write(response.read())
        time.sleep(.5)
    except urllib2.HTTPError as e:
        print ('%s' % e)
    
    mf =  mad.MadFile("/mnt/array1/Musik/texttosonos.mp3")
    return (mf.total_time()/1000)
    print 'Saved MP3 to %s' % (filee.name)
    filee.close()
    
def unicode_urlencode(params):
    '''
        Encodes params to be injected in an url.
    '''
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])

def sonos_durchsage(text):
    laenge = downloadAudioFile(text)
    #set_szene("SonosSave")
    #set_szene("Durchsage")
    time.sleep(laenge + 1)
    #set_szene("SonosReturn")    
    
if __name__ == '__main__':
        main()