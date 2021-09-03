import time
import logging
from gqlalchemy import Memgraph as memgraph_connector


log = logging.getLogger(__name__)


class Memgraph:
    def __init__(self, memgraph_host, memgraph_port):
        self.memgraph_host = memgraph_host
        self.memgraph_port = memgraph_port
        self.memgraph = self.connect_to_memgraph()

    def connect_to_memgraph(self):
        memgraph = memgraph_connector(self.memgraph_host, self.memgraph_port)
        connection_established = False
        while(not connection_established):
            try:
                if (memgraph._get_cached_connection().is_active()):
                    connection_established = True
                    log.info("Connected to Memgraph")
            except:
                log.info("Memgraph probably isn't running")
                time.sleep(4)
        return memgraph

    def load_data_into_memgraph(self, path_to_input_file):
        node = self.memgraph.execute_and_fetch(
            "MATCH (n) RETURN n LIMIT 1;"
        )
        if len(list(node)) == 0:
            self.memgraph.drop_database()
            self.memgraph.execute(
                f"""LOAD CSV FROM "{path_to_input_file}"
                        WITH HEADER DELIMITER " " AS row
                        MERGE (a:Person {{id: row.id_1}})
                        MERGE (b:Person {{id: row.id_2}})
                        CREATE (a)-[:FRIENDS_WITH]->(b);"""
            )

    def get_graph(self):
        results = self.memgraph.execute_and_fetch(
            f"""MATCH (n)-[r]-(m)
                    RETURN n as from, m AS to;"""
        )
        return list(results)
