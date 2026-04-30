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
if [ "${SKIP_COMMIT:-0}" != "1" ]; then
  git add .
  git commit -am "Sync mirrors"
fi

echo "Done"
