################
# Author:  Kunj Shah
# Date:    2024-06-01
# Description: This script defines a service application using fastapi, which calls the dynamic prompt utility to generate responses from a large language model based on user input. This application works as a backend application used as an API.
# Model: Gemini-2.5 flash
################

#import necessary libraries
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Create FastAPI instance
app = FastAPI()

#create client instance for Gemini-2.5 flash and authenticate using API key from environment variable
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

# Define a Pydantic model for the request body
class DevOpsProblem(BaseModel):
    query: str

# Define a dynamic prompt to elicit specific responses from the model based on user input
def devops_assistant(user_input):
    prompt = f"""
    You are a senior DevOps engineer.

    Problem:
    {user_input}

    Return response in this format:

    Causes:
    - ...

    Debug Steps:
    - ...

    Fixes:
    - ...
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# Define an API endpoint to receive user input and return response from the model
@app.post("/devops-assistant")
def get_devops_solution(problem: DevOpsProblem):
    response = devops_assistant(problem.query)
    return {"response": response}
