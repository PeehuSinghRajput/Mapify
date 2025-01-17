from py2neo import Graph
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Connect to the Neo4j database using details from .env file
def get_neo4j_connection():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    # Establish connection to Neo4j
    graph = Graph(uri, auth=(user, password))
    return graph