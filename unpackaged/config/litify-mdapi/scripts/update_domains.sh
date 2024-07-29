#!/bin/bash

echo "Script started"

consumerkey_value=$(cat config/consumerkey.txt)
echo "Domain value read: $consumerkey_value"

sed -i "s|CONSUMER_KEY|$consumerkey_value|g" ../src/main/default/authproviders/LitifyMDAPI.authprovider-meta.xml
echo "Replaced CONSUMER_KEY in authprovider-meta.xml"

echo "Script completed"
