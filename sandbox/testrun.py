#!/usr/bin/python

import sys
import py_compile
import module
i = 0
for j in range(0,1000):
    if((j%4 == 0) and (j%12 == 0)):
        i=i+1
print i
