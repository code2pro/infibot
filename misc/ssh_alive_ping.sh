#!/bin/bash

ssh user@remote "nohup poll_every_nsec.pl 2>&1 >/dev/null &"

ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=1 -N -R 1234:localhost:1234 user@remote