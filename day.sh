#!/usr/bin/env sh

# Ensure padding to two digits
day=$1
if [ ${#day} -eq 1 ]; then
	day="0$day"
fi

# If the file exists, do nothing
filename="advent/day${day}.py"
if [ -f "$filename" ]; then
	echo "File $filename already exists"
	exit 0
fi

# Otherwise, copy the template
cp template.py "$filename"
