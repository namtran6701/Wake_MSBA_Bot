from langchain_core.documents import Document
from pydantic import BaseModel
import requests 
import os
import streamlit as st

JINA_API_KEY = st.secrets["JINA_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

def ggsearch_reformat(result):
    """
    Reformats Google search results into a list of Document objects.

    Args:
        result (dict): The raw search result from Google Serper API.

    Returns:
        list: A list of Document objects containing formatted search results.

    This function processes both Knowledge Graph and organic search results.
    If an error occurs or no results are found, it returns a Document with an error message.
    """
    documents = []
    
    try:
        # Process Knowledge Graph results if present
        if 'knowledgeGraph' in result:
            kg = result['knowledgeGraph']
            doc = Document(
                page_content=kg.get('description', ''),
                metadata={
                    'source': kg.get('descriptionLink', ''),
                    'title': kg.get('title', ''),
                }
            )
            documents.append(doc)
        
        # Process organic search results
        if 'organic' in result:
            for item in result['organic']:
                doc = Document(
                    page_content=item.get('snippet', ''),
                    metadata={
                        'source': item.get('link', ''),
                        'title': item.get('title', ''),
                    }
                )
                documents.append(doc)
        
        # Raise an error if no results were found
        if not documents:
            raise ValueError("No search results found")
        
    except Exception as e:
        # Handle any exceptions and return an error Document
        print(f"An error occurred: {str(e)}")
        documents.append(Document(
            page_content="No search results found or an error occurred.",
            metadata={'source': 'Error', 'title': 'Search Error'}
        ))
    
    return documents

# make stream document easier
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


# scrape the web page returned by google search
def jina_scrape(site):
    """
    Scrape a website using the Jina API.

    Args:
        site (str): The URL of the website to scrape.

    Returns:
        str: The scraped content of the website.
    """
    jina_url = f'https://r.jina.ai/{site}'
    headers = {
        'Authorization': f'Bearer {JINA_API_KEY}'
    }
    
    response = requests.get(jina_url, headers=headers)
    
    return response.text
