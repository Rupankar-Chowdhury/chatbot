import datetime
import string
import json
import spacy
from flask import Flask, render_template, request

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

# Load keywords and responses from the JSON file
with open('demo.json', 'r') as f:
    json_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', prompt="Enter your query:")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    conversation = request.form.getlist('conversation[]')
    conversation.append(f"You: {user_input}")

    matched_responses = get_matched_responses(user_input)

    # Add bot responses to the conversation
    for response in matched_responses:
        conversation.append(f"Bot: {response}")

    # Update the prompt for the next user input
    prompt = "You:"

    return render_template('index.html', user_input=user_input, responses=conversation, prompt=prompt)

def get_matched_responses(user_input):

    matched_responses = []

    keywords = ['evaluate', 'claim', 'insurance', 'policy', 'risk']
    user_input_doc = nlp(user_input)

    user_keywords = sorted([token.lemma_ for token in user_input_doc if token.lemma_ in keywords])
    search_key = ' '.join(user_keywords)
    if search_key in json_data:
        matched_responses = json_data[search_key]

    return matched_responses

if __name__ == '__main__':
    app.run(debug=True)