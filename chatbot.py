import os
import nltk
import ssl
import streamlit as st
import random
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')


 #Create VECTORIZER AND CLASSIFIER
 
vectorizer = TfidfVectorizer()
classifier = LogisticRegression(random_state=0, max_iter=10000)

#preprocess the data

tags=[]
patterns=[]
for intent in intents:
    for pattern in intent ['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)
        
       
#Training the Model
x= vectorizer.fit_transform(patterns)
y=tags
classifier.fit(x, y)

#CREATE THE CHATBOT

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag= classifier.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response
        
#CHATBOT WITH STREALIT

counter=0
def main():
    global counter
    st.title("Chatbot")
    st.write("Welcome to Chatbot")
    
    counter+=1
    user_input= st.text_input("You: ", key=f"user_input_{counter}")
    
    if user_input:
        response = chatbot(user_input)
        st.text_area("Chatbot:", value=response, height=200, key=f"response_{counter}", max_chars=None)
        
        if response.lower() in ["bye", "goodbye", "see you later"]:
            st.write("Thank you for chatting! Goodbye!")
            st.stop()
            
if __name__ == "__main__":
    main()            
                    
        