#!/usr/bin/env python3

import os
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta

def main(mypath):

    files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[f.rindex('.'):] == '.pdf']

    expiryTime = datetime.now() - timedelta(seconds = 10)

    for f in files:
        createdTime = os.path.getctime(join(mypath, f))
        createdTime = datetime.fromtimestamp(createdTime)
        if createdTime < expiryTime:
            os.remove(join(mypath, f))

if __name__ == '__main__':
    main()