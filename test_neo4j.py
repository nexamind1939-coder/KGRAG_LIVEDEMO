import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

print("URI loaded:", bool(uri))
print("Username loaded:", bool(user))
print("Password loaded:", bool(password))

try:
    driver = GraphDatabase.driver(
        uri,
        auth=(user, password)
    )

    driver.verify_connectivity()

    with driver.session() as session:
        result = session.run(
            "RETURN 'Neo4j Connected!' AS message"
        )
        print(result.single()["message"])

    driver.close()

except Exception as e:
    print("Connection error:", repr(e))