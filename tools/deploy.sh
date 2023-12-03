#!/bin/bash

rsync -av ./output/ dh_ucgq4t@dawson.dreamhost.com:notes.yoshicarroll.com

# Make it executable with chmod +x deploy.sh