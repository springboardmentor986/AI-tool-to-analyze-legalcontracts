from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("AIzaSyDHDEqV294mpiQ8XWSbnbYfggXJVlHDnSU"))

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Say hello in one sentence"
)

print(response.text)
