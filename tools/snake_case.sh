#!/bin/bash

# Check if filename is provided
if [ -z "$1" ]
then
  echo "No filename provided. Usage: ./script.sh <filename>"
  exit 1
fi

original_filename="$1"
snake_case_filename=$(echo "$original_filename" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')

mv "$original_filename" "$snake_case_filename"

# You can save this script to a file, make it executable with chmod +x snake_case.sh,
# and then run it with a filename as a parameter, like 
# ./script.sh "Writing is the only thing that matters.md".