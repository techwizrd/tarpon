#!/bin/sh

autoreconf --force --install --verbose || exit 1
./configure
