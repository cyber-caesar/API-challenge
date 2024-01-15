curl -X POST -H "Content-Type: multipart/form-data" -H "x-api-key: 9d207bf0-10f5-4d8f-a479-22ff5aeff8d1" -F "file=@/home/odysseus/Downloads/Data/dog.json" http://localhost:8000/match-json

curl -X GET "http://localhost:8000/dog-list?api-key=9d207bf0-10f5-4d8f-a479-22ff5aeff8d1"


