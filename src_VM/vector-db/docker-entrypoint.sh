#!/bin/bash

echo "Container is running!!!"


#To be used for development and production
#args="$@"
#echo $args

#if [[ -z ${args} ]]; 
#then
#    pipenv shell
#else
#  pipenv run python $args
#fi

#To be used for kubernetes
if [[ $# -eq 0 ]]; then
  echo "Running default CLI script..."
  pipenv run python cli.py
else
  pipenv run python "$@"
fi