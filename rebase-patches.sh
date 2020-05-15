#!/bin/sh

# To rebas Wayland and other patches:

# Get fork:
git clone https://github.com/kraj/userland
cd userland/
git checkout kraj/master

# Get official raspberry repository data:
git remote add upstream https://github.com/raspberrypi/userland.git
git pull --all

# Get latest official commit:
git checkout upstream/master
export UPSTREAM_COMMIT_ID=$(git log --format="%H" -n 1)

# Rebase fork:
git checkout kraj/master
git rebase upstream/master

# Generate patches:
git format-patch ${UPSTREAM_COMMIT_ID}..HEAD
rm -f ../*.patch
mv *.patch ..

rm -fr userland
