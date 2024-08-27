from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()


# Define Model
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
# Cheak and Threw Error If Any Error while Loading Data
try:
    # load data using text loader
    loader = TextLoader("data.txt")
except Exception as e:  
    print("Error while loading file=", e)

# Embedding
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# chunks of data
text_splitter = CharacterTextSplitter(chunk_size=500,chunk_overlap=100)
# Create the index with the specified embedding model and text splitter
index_creator = VectorstoreIndexCreator(
    embedding=embedding,
    text_splitter=text_splitter
)
index = index_creator.from_loaders([loader])

# Query the index with the LLM
while True:
    human_message = input("What do you Wants to know about SmartHome Hub")
    response = index.query(human_message, llm=llm)
    print(response)
    if human_message == 'ok thanks':
        break

