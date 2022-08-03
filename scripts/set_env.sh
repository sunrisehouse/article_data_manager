#!/bin/bash
echo $ENV_CONTENTS > temp.env
cat temp.env
base64 --decode temp.env .env
cat .env
