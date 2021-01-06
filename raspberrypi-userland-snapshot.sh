#!/bin/sh
set -e

TARBALL=raspberrypi-userland

git clone https://github.com/raspberrypi/userland/

cd userland

COMMIT=$(git rev-list HEAD -n1)
SHORTCOMMIT=$(echo ${COMMIT:0:7})
DATE=$(git log -1 --format=%cd --date=short | tr -d \-)

cd ..

tar -cJf $TARBALL-$SHORTCOMMIT.tar.xz userland
rm -fr userland

sed -i \
    -e "s|%global commit0.*|%global commit0 ${COMMIT}|g" \
    -e "s|%global date.*|%global date ${DATE}|g" \
    $TARBALL.spec

rpmdev-bumpspec -D -c "Update to latest snapshot." $TARBALL.spec

