curl -X POST -H "Content-Type: application/json" -d '{"text":"New note","tags":["tag1","tag2"]}' http://localhost:3000/notes


curl http://localhost:3000/notes?tags=tag1
