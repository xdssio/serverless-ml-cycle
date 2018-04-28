Serverless AI is a project demonstrating how to have the entire data science cycle as serverless

# Tests
export URL=localhost:8080
curl $URL/ping -w "\n\n"
curl $URL/version -w "\n\n"
curl  -X POST $URL/train -w "\n\n"
curl -H "Content-Type: text/csv" --data-binary "@./datasets/titanic.csv" -X POST $URL/predict -w "\n\n" 
curl -H "Content-Type: application/json" -d "@./datasets/titanic.json" -X POST $URL/predict -w "\n\n" 

# Deployment

```
docker build -t serverlessai .

# one time
alias serverlessai='docker run -ti -v $(pwd):/var/task -v ~/.aws/:/root/.aws -p 8080:8080 --rm serverlessai'
alias serverlessai >> ~/.bash_profile

serverlessai:
serverlessai>  python3 -m venv ve
serverlessai> source ve/bin/activate
serverlessai> pip install -r requirements.txt
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
serverlessai> zappa deploy dev
serverlessai> zappa update dev
serverlessai> zappa undepoloy dev
serverlessai> zappa schedule dev
serverlessai> zappa unschedule dev

````


## for new data-science case
Edit the *Model* class change  *preprocessing*, and *get_data* and you are good to go.