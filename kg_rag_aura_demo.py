import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    url,
    auth=(username, password)
)

driver.verify_connectivity()

print("Neo4j Aura Connected Successfully!")