import torch
import numpy as np
import json
from nltk_utils import bag_of_words, tokenize, stem
from model1 import NeuralNet

# Load data
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Load the saved model
data = torch.load("data.pth")
model = NeuralNet(data['input_size'], data['hidden_size'], data['output_size'])
model.load_state_dict(data['model_state'])
model.eval()

# Preparing the data
all_words = data['all_words']
tags = data['tags']

# Use a subset of the 'training' data as a stand-in for testing
X_test = []
y_test = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        xy.append((w, tag))

# Convert sentences into bag of words format
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_test.append(bag)
    y_test.append(tags.index(tag))

X_test = np.array(X_test)[-int(len(X_test) * 0.3):]  # Take last 30% of data
y_test = np.array(y_test)[-int(len(y_test) * 0.3):]

# Evaluate the model
correct = 0
total = len(X_test)
with torch.no_grad():
    for i in range(total):
        output = model(torch.from_numpy(X_test[i]).float().unsqueeze(0))
        _, predicted = torch.max(output, 1)
        correct += (predicted == y_test[i]).sum().item()

accuracy = 100 * correct / total
print(f'Accuracy of the model on the test data: {accuracy:.2f}%')




