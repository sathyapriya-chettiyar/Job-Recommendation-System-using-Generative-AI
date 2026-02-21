import fitz 
import os 
from dotenv import load_dotenv
#from openai import OpenAI
import requests


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


#client = OpenAI(api_key=OPENAI_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    
    Args:
        uploaded_file (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_llm(prompt):
    """
    Sends a prompt to the local Ollama model and returns the response.
    
    Args:
        prompt (str): The prompt to send to the LLM.
        
    Returns:
        str: The response from the Ollama model.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",  # Lightweight, 2.2 GB model
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        return response.json()["response"]
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama server: {str(e)}"
# def ask_openai(prompt, max_tokens=500):
#     """
#     Sends a prompt to the OpenAI API and returns the response.
    
#     Args:
#         prompt (str): The prompt to send to the OpenAI API.
#         model (str): The model to use for the request.
#         temperature (float): The temperature for the response.
        
#     Returns:
#         str: The response from the OpenAI API.
#     """
#     try:
#         response = client.chat.completions.create(
#             model='gpt-4o-mini',#'gpt-4o',#"gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.5,
#             max_tokens=max_tokens
#         )
#         return response.choices[0].message.content
    
#     except RateLimitError:
#         return "OpenAI quota exceeded. Please check billing or try again later."

    