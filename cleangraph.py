# from neo4j import GraphDatabase

# class Neo4jConnection:
#     def __init__(self, uri, user, pwd):
#         self.driver = GraphDatabase.driver(uri, auth=(user, pwd))

#     def close(self):
#         self.driver.close()

#     def clean_graph(self):
#         with self.driver.session() as session:
#             session.write_transaction(self._delete_all)

#     def query(self, query, parameters=None):
#         with self.driver.session() as session:
#             return session.run(query, parameters)

#     @staticmethod
#     def _delete_all(tx):
#         tx.run("MATCH (n) DETACH DELETE n")

# # Example usage
# conn = Neo4jConnection("neo4j+s://63bac5fe.databases.neo4j.io:7687", "neo4j", "dqJM4lwB7qi35Qq5A1OT1I46EuuXEbO8heLO79fDa9s")

# try:
#     result = conn.query("MATCH (n) RETURN n LIMIT 5")
#     # Directly iterate over the result
#     for record in result:
#         print(record)  # This will print each record in the result
# finally:
#     conn.close()



from neo4j import GraphDatabase
import os
from dotenv import load_dotenv


class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, pwd))
            # Verify connection
            self.driver.verify_connectivity()
            print("Connected to Neo4j database successfully!")
        except Exception as e:
            print(f"Failed to connect to the database: {str(e)}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()

    def clean_graph(self):
        with self.driver.session(database="neo4j") as session:  # Specify database name
            session.execute_write(self._delete_all)

    def query(self, query, parameters=None):
        try:
            with self.driver.session(database="neo4j") as session:  # Specify database name
                result = session.run(query, parameters or {})
                return list(result)  # Convert result to list for easier handling
        except Exception as e:
            print(f"Query failed: {str(e)}")
            raise

    @staticmethod
    def _delete_all(tx):
        tx.run("MATCH (n) DETACH DELETE n")

def main():

    load_dotenv()
    uri = os.getenv("NEO4J_URL")
    user = os.getenv("NEO4J_USERNAME")
    pwd = os.getenv("NEO4J_PASSWORD")

    try:
        # Create connection
        conn = Neo4jConnection(uri, user, pwd)
        
        # Execute query
        result = conn.query("MATCH (n) RETURN n LIMIT 5")
        
        # Process results
        for record in result:
            print(record)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Always close the connection
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()