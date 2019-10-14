#!/bin/sh

# Exit immediately any command returns a non-zero status
set -ex

# The following script exports all the collections of a mongo database to json
# files into the data directory
#
# Usage:
#     ./initiate-database.sh <database_name> <data_directory>"

usage()
{
    echo "usage: ./export-database.sh <database_name> <data_directory"
}

if [ $# -gt 1 ]; then
    collectionName=$1
    dataDirectory=$2
else
    echo "Error: wrong number of parameters"
    usage
    exit 1
fi

if ! [ -x "$(command -v mongo)" ]; then
  echo 'Error: mongo is not installed.' >&2
  echo 'Install it first'
  exit 1
fi

allJsonFiles=($(ls $dataDirectory))

echo "$dataDirectory contains ${#allJsonFiles[@]} json files"
for filename in "${allJsonFiles[@]}";
do
  echo "Importing $filename"
  mongoimport --db $collectionName --quiet --file "$dataDirectory/$filename"
done
