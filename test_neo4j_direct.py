
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)

try:
    driver.verify_connectivity()
    print("Aura authentication successful!")

    with driver.session(database="USERNAME") as session:
        result = session.run(
            "RETURN 'Hello Neo4j Aura!' AS message"
        )
        print(result.single()["message"])

except Exception as e:
    print("Error:", type(e).__name__, str(e))

finally:
    driver.close()
