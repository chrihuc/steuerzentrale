#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christoph
"""
#!/usr/bin/env python

import pycurl



conn = pycurl.Curl()
#scenes = szenen.Szenen()


def on_receive(data):
    data = data.decode()
    print(data)
    return -1

def main():
    conn.setopt(pycurl.URL, "192.168.192.4/control?callback=cname&cmd=subscribe&format=txt")
    conn.setopt(pycurl.WRITEFUNCTION, on_receive)
    #aes.new_event(description="XS1inputs neugestartet", prio=0)
    conn.perform()


if __name__ == '__main__':
    main()
