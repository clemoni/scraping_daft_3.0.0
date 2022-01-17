#!/bin/bash
cd ~/Development/Projects/scraping_daft/scraping_daft_3.0.0/ 
docker-compose down 
sleep 30
docker container ls 
test -z "$(docker ps -q 2>/dev/null)" && osascript -e 'quit app "Docker"'

