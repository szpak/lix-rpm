#!/bin/bash
# we want a local dep-file for every new version

VERS=0.10.35

if [ ! -d LixD-${VERS} ]; then
    tar -zxf LixD-${VERS}.tar.gz
fi

cd LixD-${VERS}
DUB_HOME=./lix-dub-deps-local-${VERS} dub upgrade
tar -Jcvf ../lix-dub-deps-local-${VERS}.tar.xz lix-dub-deps-local-${VERS}

