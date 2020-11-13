#!/bin/bash

set -e

CHDIR="./certs"

rm -rf $CHDIR
mkdir -p $CHDIR

echo "Generating self-signed root CA"
openssl genrsa -out $CHDIR/ca.key 2048
openssl req -new -subj "/C=KR" -x509 -days 365 -key $CHDIR/ca.key -sha256 -out $CHDIR/ca.crt
