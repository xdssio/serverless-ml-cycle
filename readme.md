Serverless AI is a project demonstrating how to have the entire data science cycle as serverless

# Tests
export URL=localhost:8080
curl $URL/ping -w "\n\n"
curl $URL/version -w "\n\n"
curl  -X POST $URL/train -w "\n\n"
curl -H "Content-Type: text/csv" --data-binary "@./datasets/titanic.csv" -X POST $URL/predict -w "\n\n" 
curl -H "Content-Type: application/json" -d "@./datasets/titanic.json" -X POST $URL/predict -w "\n\n" 
