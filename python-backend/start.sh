#! /bin/bash

while getopts ':bdt' opt; do
  case $opt in
    b) 
      docker-compose build --no-cache >&2
      ;;
    d)
      docker-compose --env-file ./configuration/.env.mongo.dev up >&2
      ;;
    t)
      docker-compose --env-file ./configuration/.env.mongo.test up >&2
      ;;
    \?)
      echo 'Invalid option: -$OPTARG' >&2
      ;;  
  esac 
done