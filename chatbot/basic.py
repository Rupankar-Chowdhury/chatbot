import datetime
import string
import json
import spacy
from flask import Flask, render_template, request

user_dict = {
    1:"Soumya De",
    2:"Rupankar Chowdhury",
    3:"Swarnali Saha",
    4:"Anushka Das",
    5:"Aratrika Ray",
}

nlp = spacy.load("en_core_web_sm")

current_time = datetime.datetime.now()
current_hour = current_time.hour

print(
        ("Good morning ! " if 6 <= current_hour < 12 else
         "Good afternoon ! " if 12 <= current_hour < 18 else
         "Good evening ! ")
    )

keywords = ['evaluate', 'claim', 'insurance', 'policy', 'risk']


with open('./demo.json', 'r') as f:
    json_data = json.load(f)
    while True:

        user_input = input("Enter your query (type 'q' to quit): ")
        print()
        user_input_doc = nlp(user_input)

        if user_input.lower() == 'q':
            break  # Exit the loop if 'q' is entered

        user_keywords = sorted([token.lemma_ for token in user_input_doc if token.lemma_ in keywords])
        search_key = ' '.join(user_keywords)
        question_set = json_data.get(search_key)

        print(question_set)
        matched_responses = []

        if question_set:
            if len(user_keywords) == len(keywords):
                for question in question_set:
                    print(question)
                    # Basically inputting the policy and claim number 
                    input("Write your answer: ")
            
            else:
                print("Did you mean --> (Select one from below): ")
                print()
                for question in question_set:
                    print(question)
                    matched_responses.extend(question)
                print()
                # Select an option from the above questions
            print(matched_responses)
        else:
            print("I dont understand! :( Try again.")