### Create a shared folder for installing libraries
mkdir -p shared/python

### Install libraries from requirements.txt into shared/python
pip install -r requirements.txt -t shared/python

cp -r shared_files shared/python/

sam validate

sam build

sam package \
  --s3-bucket b2c-logger \
  --output-template-file out.yml \
  --region ap-south-1

sam deploy \
  --template-file out.yml \
  --stack-name b2c \
  --region ap-south-1 \
  --no-fail-on-empty-changeset \
  --capabilities CAPABILITY_IAM

rm -r shared