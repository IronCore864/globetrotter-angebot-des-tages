#!/bin/bash
rm function.zip
pip install --target ./package -r requirements.txt
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py
aws lambda update-function-code --function-name test --zip-file fileb://function.zip
