from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.driver = GraphDatabase.driver(uri, auth=(user, pwd))

    def close(self):
        self.driver.close()

    def clean_graph(self):
        with self.driver.session() as session:
            session.write_transaction(self._delete_all)

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters)

    @staticmethod
    def _delete_all(tx):
        tx.run("MATCH (n) DETACH DELETE n")

# Example usage
conn = Neo4jConnection("neo4j+s://87b94088.databases.neo4j.io", "neo4j", "VOQwjC2G0HdFu80UwMs5-K0Ky8S0HeD5b4bFIDUUOmY")

try:
    result = conn.query("MATCH (n) RETURN n LIMIT 5")
    # Directly iterate over the result
    for record in result:
        print(record)  # This will print each record in the result
finally:
    conn.close()
