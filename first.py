from transformers import pipeline

classifier = pipeline("sentiment-analysis")
print(classifier(["This is a happy day"]))
