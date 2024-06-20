import os
import json
import pymongo
from typing import List
from langchain.agents import Tool
from langchain.tools import StructuredTool
from langchain.schema.document import Document
from langchain.vectorstores import AzureCosmosDBVectorSearch

CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

AOAI_ENDPOINT_CHAT = os.getenv("AOAI_ENDPOINT_CHAT")
AOAI_KEY_CHAT = os.getenv("AOAI_KEY_CHAT")

AOAI_ENDPOINT_EMBEDDING = os.getenv("AOAI_ENDPOINT_EMBEDDING")
AOAI_KEY_EMBEDDING = os.getenv("AOAI_KEY_EMBEDDING")

AOAI_API_VERSION = os.getenv("AOAI_API_VERSION")

EMBEDDINGS_DEPLOYMENT_NAME = os.getenv("EMBEDDINGS_DEPLOYMENT_NAME")
COMPLETIONS_DEPLOYMENT_NAME = os.getenv("COMPLETIONS_DEPLOYMENT_NAME")

db = pymongo.MongoClient(CONNECTION_STRING).db



# Create course and degree retrievers

embedding_model = AzureOpenAIEmbeddings(
    openai_api_version = AOAI_API_VERSION,
    azure_endpoint = AOAI_ENDPOINT_EMBEDDING,
    openai_api_key = AOAI_KEY_EMBEDDING,   
    azure_deployment = EMBEDDINGS_DEPLOYMENT_NAME,
    chunk_size=10)

def create_retriever(collection: str, top_k: int = 3,):
    vector_store =  AzureCosmosDBVectorSearch.from_connection_string(
        connection_string = CONNECTION_STRING,
        namespace = f"db.{collection}",
        embedding = EMBEDDINGS_DEPLOYMENT_NAME,
        index_name = "VectorSearchIndex",
        embedding_key = "embedding",
        text_key = "_id")
    return vector_store.as_retriever(search_kwargs={"k": top_k})

degrees_retriever = create_retriever("degrees")
courses_retriever = create_retriever("calendar_courses")


# Define tools

def filter_dict(di, keys):
    return {k: v for k, v in di.items() if k in keys}

def annotate_dict(di):
    return ", ".join([str(k) + ": " + str(v) for k, v in di.items()])


def format_course_doc(docs: List[Document]) -> str:
    """Format the course docs."""
    return ", ".join([annotate_dict(filter_dict(doc.metadata, ['_id', 'name', 'description']))
                      for doc in docs])

def format_degree_doc(docs: List[Document]) -> str:
    """Format the degree docs."""
    return ", ".join([annotate_dict(filter_dict(doc.metadata, ['title', 'description']))
                      for doc in docs])

degrees_retriever_chain = degrees_retriever | format_degree_doc
courses_retriever_chain = courses_retriever | format_course_doc

# tools = [courses_retriever.create_retriever_tool]
tools = [Tool(name = "vector_search_degrees", 
              func = degrees_retriever_chain.invoke,
              description = "Find degrees similar to the question."),
         Tool(name = "vector_search_courses", 
              func = courses_retriever_chain.invoke,
              description = "Find courses similar to question.")]

def get_course_by_id(code: str) -> str:
    """
    Retrieves a course by it's course code, eg: MATH101
    """
    code = code.replace(' ', '')
    doc = db.calendar_courses.find_one({"_id": code})  
    if doc:
        return json.dumps({'code': doc['_id'], 'name': doc['name'], 'description': doc['description']})
    else:
        return ""

def get_course_prerequisites(code: str) -> str:
    """
    Retrieves a courses prerequisites by it's course code, eg: MATH101
    """
    code = code.replace(' ', '')
    doc = db.calendar_courses.find_one({"_id": code})
    return json.dumps(doc['prerequisites'].values(), default=str)

def get_degree_by_title(title: str) -> str:
    """
    Retrieves a degree by it's name, eg: Mathematics
    """
    doc = db.degrees.find_one({"title": title})
    return json.dump({'code': doc['_id'],
                      'title':title, 
                      'description': doc['description'],
                      'required course list': ', '.join(doc['requirementCourseList'])})

def determine_course_offering(code: str) -> str:
    """
    Find if a course is offered
    """
    code = code.replace(' ', '')
    doc = db.courses.find_one({"_id": code})
    print(doc)
    if doc:
        sections = doc.get('sections')
        out_sec = []
        if sections:
            for sec in sections:
                out_sec.append({'start': sec['start'],
                                'end': sec['end'],
                                'start_date': sec['startDate'],
                                'days': sec['days'],
                                'seq': sec['seq']})

        return json.dumps({"is_offered": "yes", 'sections': out_sec})
    else:
        return json.dumps({"is_offered": "no"})



degrees_retriever = create_retriever("degrees")
courses_retriever = create_retriever("calendar_courses")
tools.extend([StructuredTool.from_function(get_course_by_id, description="useful for finding information about a specific course when you have the subject and course number"),
              StructuredTool.from_function(get_course_prerequisites, description="useful when asked about requirements for a course"),
              StructuredTool.from_function(get_degree_by_title, description="useful when looking for information about a specific degree"),
              StructuredTool.from_function(determine_course_offering, description="useful for finding if a course is offered and getting details about it's upcoming sections")])