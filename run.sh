#!/bin/sh

cd bot
if [ -z ${DOMAIN+x} ];
then
echo "Domain name was not provided";
else
echo "Domain name is $DOMAIN";
FILE=./certs/YOURPRIVATE.key
if [ -f "$FILE" ]; then
  echo "Keys exists"
else
  echo "$FILE does not exist. Generating certificate"
  mkdir certs
  openssl req -newkey rsa:2048 -sha256 -nodes -keyout ./certs/YOURPRIVATE.key -x509 -days 365 -out ./certs/YOURPUBLIC.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=$DOMAIN"
fi
fi
python main.py;
