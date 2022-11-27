# AWS SAM With Fast-API

A sample repository to build and deploy your Fast-API app using [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) ( Serverless Application Model )

# Pre-requisites
AWS resources you will be needing for this project
1) AWS Cloudformation
2) AWS S3
3) AWS Lambda function & layers
4) AWS API Gateway
5) AWS IAM ( for configuring user & roles )

Libraries required in your system to run this project
1) Python >= 3.8 - ( we are using 3.9 here )
2) AWS Account ( including AWS CLI Installed )
3) AWS SAM CLI
4) Docker ( Optional )
5) VS Code

**References**:
1) [AWS CLI Quick Setup](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)

**Note**: Make sure you have required roles and policy attached for the user ( configured for AWS CLI ) to execute SAM process successfully

# Steps
1) Clone this repo to your system
2) Open the repo folder with VS Code
3) Open a terminal in VS Code and change the directory to root of the project
4) Set-up a virtual environment for your project
```console
user@:~$ pip install virtualenv
user@:~$ virtualenv -p python3.9 venv
```
5) Install all the libraries from requirements.txt
```console
user@:~$ pip install -r requirements.txt
```
6) Once making changes under the app folder, you can start deploying using SAM
7) ( Optional ) validate your SAM template
```console
user@:~$ sam validate
```
8) Build your app using SAM
```console
user@:~$ sam build --use-container
## You can use {--use-container to build using docker}
```
9) Package your application
```console
user@:~$ sam package \
--s3-bucket {bucket-name} \
--output-template-file out.yml \
--region {region}
```
10) Finally deploy your SAM template
```console
user@:~$ sam deploy \
--template-file out.yml \
--stack-name {cloudformation-stack-name} \
--region {region} \
--no-fail-on-empty-changeset \
--capabilities CAPABILITY_IAM \
```
11) You can check your AWS account for your resources being created
**Note**: Also ensure that your cloudformation stack is created with the resources mentioned with SAM template