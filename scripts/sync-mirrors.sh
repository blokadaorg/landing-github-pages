#!/bin/sh

echo "Syncing all mirrors"

cd ../tracker-radar
git checkout main
git pull

cd ../scripts
./ddg.py
./exodus.py
./mirror.py

cd ..
git add .
git commit -am "Sync mirrors"

echo "Done"
