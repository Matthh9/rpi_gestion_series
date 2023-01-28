# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 05:34:05 2022

@author: matth
"""
import sys
import urllib.request


if __name__ == '__main__':
    #print ('sys.argv: ', sys.argv)
    if len(sys.argv) > 1:
        print(sys.argv[1], sys.argv[2])
        
        try:
            urllib.request.urlretrieve(sys.argv[1], sys.argv[2])
            print(1)
        except :
            print(0)
    else:
        print(0)
