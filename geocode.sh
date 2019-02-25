#!/bin/sh

CWD="$(cd "$(dirname "$0")" && pwd)"
cd $CWD

LC_ALL=C.UTF-8 ./geocode.py $*
