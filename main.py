#streamlit
import streamlit as st

# base stack
import os
import pickle
import pandas as pd
import json

# custom made functions and Load environment variables from .env file
from dotenv import load_dotenv
import sys
sys.path.insert(1, '..\\')
load_dotenv()
from utils.funcs import show_ui

#langchain stack 
## OpenAI + OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

## Vector Store
from langchain_community.vectorstores import Chroma

## Retriever
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

from langchain_openai import OpenAIEmbeddings

# Retrieve the API key and initialize client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = openai_api_key)

# create the open-source embedding function
embedding_function = OpenAIEmbeddings()

# other environment variables
PATH_HIERARCHIES = "../hierarchies/"

# Load the list from a file using pickle
with open('output\jsons_metadata.pkl', 'rb') as file:
    jsons = pickle.load(file)

# Load the list from a file using pickle
with open('output\jsons_metadata.pkl', 'rb') as file:
    jsons_meta = pickle.load(file)

# Load examples
json_descriptive = []
for item in jsons:
    new_json = {key: item[key]
                     for key in ['filename', 'topic']}
    json_descriptive.append(new_json)

pd_descriptive = pd.DataFrame.from_dict(json_descriptive)
descriptions = pd.read_csv('enrico/xui-caption.csv', sep='\t')
pd_descriptive['file'] = pd_descriptive['filename'].map(lambda x: int(x.replace('.json','')))
file_caption = pd.merge(pd_descriptive, descriptions, left_on='file', right_on='image_id')

# remove unknown captions
mask = file_caption['caption'].str.contains(r'unknown', na=True)
relevant_captions = file_caption[~mask].copy()

examples = []
for json_file in jsons:
    if json_file['filename'] in (list(relevant_captions['filename'])):
        mask = relevant_captions[relevant_captions['filename']==jsons[0]['filename']].index
        examples.append({'question': relevant_captions.loc[mask,'caption'].values[0]
                         , 'answer': str(json_file['content']).replace('{','«').replace('}','»')})

# generate example
example_selector = SemanticSimilarityExampleSelector.from_examples(
    # This is the list of examples available to select from.
    examples,
    # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
    Chroma,
    # This is the number of examples to produce.
    k=5,
)

example_prompt = PromptTemplate(
    input_variables=["question", "answer"], template="Question: {question}\n{answer}"
)


# Function that generates the results
def return_results(user_prompt):
    prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        suffix="Question: {input}",
        input_variables=["input"],
    )

    result = prompt.format(input=f"{user_prompt}")
    selected_examples =example_selector.select_examples({"question": user_prompt})

    file_name = jsons_meta[examples.index(selected_examples[0])]['filename']
    with open(f'hierarchies/{file_name}', 'rb') as file:
        json_data = json.load(file)
    fig = show_ui(json_data)

    return eval(result.split('\n')[1].replace('«','{').replace('»','}')), fig


# Input Streamlit
prompt_user = st.chat_input("Please provide a description of a UI")
if prompt_user:
    st.write(f"{prompt_user}")
    view , fig = return_results(prompt_user)
    st.write("""Below is an example of a View Hierarchy Structure and of a similar Hierarchy Structure""")
    st.json(view, expanded=True)
    st.pyplot(fig)
#Above is an example of a View Hierarchy Structure and of a similar Hierarchy Structure

##I want a screen that has at least two buttons at the bottom part