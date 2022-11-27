@REM CALL sam validate ( Optional )

CALL sam build --use-container

CALL sam package ^
  --s3-bucket b2c-logger ^
  --output-template-file out.yml ^
  --region ap-south-1

CALL sam deploy ^
  --template-file out.yml ^
  --stack-name b2c ^
  --region ap-south-1 ^
  --no-fail-on-empty-changeset ^
  --capabilities CAPABILITY_IAM ^