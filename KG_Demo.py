import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain

load_dotenv()

# ---------------------------------------------------------
# STEP 1: Document Loader & Chunking
# (Using sample text here so you can run it immediately;
#  swap in PyPDFLoader("file.pdf").load() for PDFs)
# ---------------------------------------------------------
raw_text = """
Ananya Sharma is the Chief Architect at GreenGrid Energy, a renewable energy startup 
headquartered in Bengaluru. In 2025, GreenGrid Energy partnered with SolarTech India 
to build a 50 MW microgrid project in Karnataka. Vikram Rao leads the hardware division 
at SolarTech India and reports directly to Ananya Sharma on the microgrid integration.
"""

docs = [Document(page_content=raw_text.strip())]
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Loaded {len(chunks)} document chunk(s).")

# ---------------------------------------------------------
# STEP 2 & 3: Entity Extraction & Relationship Mapping
# ---------------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Person", "Company", "Project", "Location"],
    allowed_relationships=[
        "WORKS_AT",
        "HEADQUARTERED_IN",
        "PARTNERED_WITH",
        "BUILDS",
        "LOCATED_IN",
        "REPORTS_TO",
    ],
)

graph_documents = transformer.convert_to_graph_documents(chunks)
print("\nExtracted Nodes:", graph_documents[0].nodes)
print("Extracted Relationships:", graph_documents[0].relationships)

# ---------------------------------------------------------
# STEP 4: Graph Storage (Neo4j AuraDB)
# ---------------------------------------------------------
graph = Neo4jGraph(
    url=os.environ["NEO4J_URI"],
    username=os.environ["NEO4J_USERNAME"],
    password=os.environ["NEO4J_PASSWORD"],
)

# Optional: clear previous demo nodes before inserting
graph.query("MATCH (n) DETACH DELETE n")

# Save nodes & relationships to AuraDB
graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)
graph.refresh_schema()
print("\nGraph Schema in Neo4j:\n", graph.schema)

# ---------------------------------------------------------
# STEP 5: Graph Query (Natural Language -> Cypher -> Answer)
# ---------------------------------------------------------
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,                # Prints the generated Cypher query
    allow_dangerous_requests=True,
)

question = "Who does Vikram Rao report to, and where is that person's company headquartered?"
response = chain.invoke({"query": question})
print("\nFinal Answer:", response["result"])