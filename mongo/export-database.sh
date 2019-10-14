#!/bin/sh

# Exit immediately any command returns a non-zero status
set -ex

# The following script exports all the collections of a mongo database to json
# files into the data directory
#
# Usage:
#     ./export-database.sh <database_name>"

usage()
{
    echo "usage: ./export-database.sh <database_name>"
}

if [ $# -gt 0 ]; then
    collectionName=$1
else
    echo "Error: missing collection name"
    usage
    exit 1
fi

if ! [ -x "$(command -v mongo)" ]; then
  echo 'Error: mongo is not installed.' >&2
  echo 'Install it first'
  exit 1
fi

relative="`dirname \"$0\"`"
THIS="`( cd \"$relative\" && pwd )`"
TARGET_DIRECTORY=$THIS/data
mkdir -p $TARGET_DIRECTORY

allCollections=($(mongo $collectionName --quiet --eval "db.getCollectionNames()" | tr -d '[],' | tr -d '"'))

echo "$collectionName contains ${#allCollections[@]} collections"
for collection in "${allCollections[@]}";
do
  echo "Exporting $collection"
  mongoexport --db $collectionName --quiet --pretty --collection $collection --out "$TARGET_DIRECTORY/$collection.json"
done
