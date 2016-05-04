#! /bin/bash

echo -n "{'Command':'Powerfailure'}" | nc -4u -q1 192.168.192.10 5000