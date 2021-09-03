import mgp
import json


@mgp.transformation
def friendship(messages: mgp.Messages
               ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        relationship_info = json.loads(message.payload().decode('utf8'))
        result_queries.append(
            mgp.Record(
                query=("MERGE (a:Person {id: $id_1}) "
                       "MERGE (b:Person {id: $id_2}) "
                       "CREATE (a)-[:FRIENDS_WITH]->(b) "),
                parameters={
                    "id_1": relationship_info["id_1"],
                    "id_2": relationship_info["id_2"]}))

    return result_queries
