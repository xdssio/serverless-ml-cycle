Serverless AI is a project demonstrating how to have the entire data science cycle as serverless


## Deployment
```
docker build -t serverlessml .

# one time
alias serverlessml='docker run -ti -v $(pwd):/var/task -v ~/.aws/:/root/.aws -p 8080:8080 --rm serverlessml'
alias serverlessml >> ~/.bash_profile

serverlessml:
serverlessml>  virtualenv ve
serverlessml> source ve/bin/activate
serverlessml> pip install pip==9.0.3
serverlessml> pip install -r requirements.txt
serverlessml> find . -name \*.pyc -delete

# test
serverlessml> python app.py
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
you can run locally from docker or in a virtual environment:   
`python app.py`

```
export URL=localhost:8080 # for testing locally
export URL=https://ptw0khsn6l.execute-api.eu-west-1.amazonaws.com/dev
curl $URL/ping -w "\n\n"
curl $URL/version -w "\n\n"
curl  -X POST $URL/train -w "\n\n"
curl -H "Content-Type: text/csv" --data-binary "@./datasets/titanic.csv" -X POST $URL/predict -w "\n\n" 
curl -H "Content-Type: application/json" -d "@./datasets/titanic.json" -X POST $URL/predict -w "\n\n" 
```


## for new data-science case
1. Edit the necessary changes in *zappa_settings.json* file
2. Edit the *Pipeline* in *ml/pipeline* and the *Model* class change *preprocessing*, and *get_data* and you are good to go
* don't forget to change the *requirements.txt* if you use other libraries