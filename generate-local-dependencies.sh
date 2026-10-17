#!/bin/bash
# we want a local dep-file for every new version

VERS=`rpmspec -q --queryformat="%{version}" --srpm lix.spec`

if [ ! -d LixD-${VERS} ]; then
    tar -zxf LixD-${VERS}.tar.gz
fi

cd LixD-${VERS}
DUB_HOME=./lix-dub-deps-local-${VERS} dub upgrade
tar -Jcvf ../lix-dub-deps-local-${VERS}.tar.xz lix-dub-deps-local-${VERS}

