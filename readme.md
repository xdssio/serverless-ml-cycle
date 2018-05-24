Serverless AI is a project demonstrating how to have the entire data science cycle as serverless
#setup 

## AWS setup 
1. Create three buckets in AWS S3
* For the lambda function
* For the models versions
* For the dataset
2. Create an IAM role

## Local setup
1. clone me repo.
2. Create virtual environment and install the requirements 
3. In the zappa settings, change the s3_bucket to your lambda bucket
4. Explore the notebook and build your pipeline.
5. edit the *ml.pipeline* file, the *zappa_settings.json* file the config as needed.

## Virtual environment instructions 
```
virtualenv ve
source ve/bin/activate
pip install pip==9.0.3
pip install -r requirements.txt
zappa update dev

# test locally
python app.py
```

# zappa
in zappa_settings.json change:  
* project_name
* s3_bucket
* models_bucket
* models_bucket
* data_key
* model_name
* data_bucket

```
serverlessml> zappa deploy dev
serverlessml> zappa update dev
serverlessml> zappa undeploy dev
serverlessml> zappa schedule dev
serverlessml> zappa unschedule dev

````


## Tests
`pytest ./tests/test.py`z


## Run server locally   
`python app.py` 

```
export URL=localhost:8080
```



### test locally
```
export URL=https://ptw0khsn6l.execute-api.eu-west-1.amazonaws.com/dev
curl $URL/ping -w "\n\n"
curl $URL/version -w "\n\n"
curl  -X POST $URL/train -w "\n\n" 
curl -H "Content-Type: application/json" -d "@./datasets/titanic.json" -X POST $URL/predict -w "\n\n" 
```

### test on lambda
```
export URL=<your apigateway url>
curl $URL/ping -w "\n\n"
curl $URL/version -w "\n\n"
curl  -X POST $URL/train -w "\n\n" 
curl -H "Content-Type: application/json" -d "@./datasets/titanic.json" -X POST $URL/predict -w "\n\n" 

```

## for new data-science case
1. Edit the necessary changes in *zappa_settings.json* file
2. Edit the *Pipeline* in *ml/pipeline* and the *Model* class change *preprocessing*, and *get_data* and you are good to go
* don't forget to change the *requirements.txt* if you use other libraries


# DEMO
export URL=https://u3inrapt1c.execute-api.eu-west-1.amazonaws.com/demo
export URL=https://uvurxdi901.execute-api.eu-west-1.amazonaws.com/dev
curl -H "Content-Type: application/json" -d "@./datasets/titanic.json" -X POST $URL/predict -w "\n\n"