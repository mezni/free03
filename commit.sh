#!/bin/bash
# VERSION=0.0.1
# ./commit.sh $VERSION "Init" 
# Module name
MODULE="wovoka"

VERSION=$1
MESSAGE=$2

# Current date
DATE=$(date +%Y-%m-%d)

# Increment patch version
# PATCH=$(date +%Y%m%d)
#PATCH=$(uuidgen | tr -d '-' | cut -c 1-8)
#VERSION="v0.0.$PATCH"
#echo $VERSION
# Clean tags
#git tag -d $(git tag)
#git push origin --delete $(git tag)

# Git operations
git add .
#git commit -m "$MODULE $DATE (version=$VERSION)"
git commit -m "$DATE/$VERSION $MESSAGE"
git push origin main
#git tag $VERSION
#git push origin main $VERSION 