#!/bin/bash

ping -c 5 172.19.47.255|grep 'bytes from'|awk '{print $4}'|cut -d: -f1|sort -u > temp.txt
