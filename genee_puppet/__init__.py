# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import sys
import os
import getopt

def usage():
    print("genee-puppet init")
    print("genee-puppet run [-n name] [-p port]")
    print("    default: name=puppetmaster, port=8140")

def puppet_init():
    os.mkdir("conf.d")
    os.mkdir("ssl.d")

def puppet_run():

    try:
        opts, args = getopt.getopt(sys.argv[2:], "n:p:")
    except getopt.GetoptError as e:
        print(str(e))

    name = 'puppetmaster'
    port = 8140
    
    for o, a in opts:
        if o == "-n":
            name = a
        elif o == "-p":
            port = int(a)

    try:
        cmd = ("docker run --name %s -d --restart=always -v %s:/opt/puppet -v %s:/var/lib/puppet/ssl -v /dev/log:/dev/log -p %d:8140 genee/puppetmaster" % (name, os.getcwd() + '/conf.d', os.getcwd() + '/ssl.d', port))
        print(cmd + "\n")
        print(subprocess.check_output(cmd, shell=True, universal_newlines=True))
    except subprocess.CalledProcessError as e:
        return

def main():

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == 'init':
        puppet_init()
    elif sys.argv[1] == 'run':
        puppet_run()

if __name__ == "__main__":
    main()