#!/bin/sh

ALBUMS=https://jsonplaceholder.typicode.com/photos

curl -s -o- $ALBUMS?albumId=$1 |
	jq -r '.[] | "\(.id) \(.title)"' |
	sort -n |
	sed 's/^[0-9]*/[&]/'
