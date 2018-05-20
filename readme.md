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
serverlessml> pip install --no-binary -U numpy
serverlessml> pip install --no-binary -U pandas
serverlessml> pip install --no-binary -U sklearn
serverlessml> pip install --no-binary -U sklearn_pandas
serverlessml> pip install flask zappa boto3
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
you can run locally with:   
`python app.py`

```
export URL=localhost:8080 # for testing locally
export URL=https://gfjbjoo9b4.execute-api.eu-west-1.amazonaws.com/dev
curl $URL/ping -w "\n\n"
curl $URL/version -w "\n\n"
curl  -X POST $URL/train -w "\n\n"
curl -H "Content-Type: text/csv" --data-binary "@./datasets/titanic.csv" -X POST $URL/predict -w "\n\n" 
curl -H "Content-Type: application/json" -d "@./datasets/titanic.json" -X POST $URL/predict -w "\n\n" 
```


## for new data-science case
Edit the *Model* class change  *preprocessing*, and *get_data* and you are good to go.