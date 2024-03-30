import streamlit as st
import pandas as pd
import openai
import json
import pandas as pd

import os
API_KEY = ""
RESOURCE_ENDPOINT = ""
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = ""
os.environ["OPENAI_API_BASE"] = RESOURCE_ENDPOINT
os.environ["OPENAI_API_KEY"] = API_KEY

openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
openai.api_version = ""


import docx2txt
from PyPDF2 import PdfReader

def read_file(file_path):
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

def extract_data_from_resume(file_path):
    resume_text = read_file(file_path)
    prompt = '''Act like a resume parser, understand given resume context, Please extract the following key-value pairs from the resume:
    If any of the information is not present in the resume, please return a message like not present.
    Always return your
        response as a valid JSON string. The format of that string should be this, 
        {
            "Name": "abc",
            "Mobile Number": "999999999",
            "Email Address": "abc@gmail.com",
            "Education": "BE, Mtech",
            "Employments": "abc, def",
            "Certifications":"data science, machine learning",
            "skills": "Python, data science",
            "Company names":"capgemini, wipro, hcl",
            "college names":"abcd"
        }
    Resume:
    '''

    response = openai.ChatCompletion.create(
        model="gpt-35-turbo",
        deployment_id="gpt-turbo",
        messages=[{"role": "user", "content": prompt + resume_text}]
    )
    content = response.choices[0]['message']['content']

    try:
        data = json.loads(content)
        return data
    except (json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
        "Measure": ["Name", "Mobile Number", "Email Address", "Education", "Employments","Certifications","skills","Company names","college name"],
        "Value": ["", "", "", "", "","","","",""]
    })