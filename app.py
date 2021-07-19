import logging
import json
import time
from pathlib import Path
from argparse import ArgumentParser
from functools import wraps
from flask import Flask, Response, render_template
from gqlalchemy import Match, Memgraph


log = logging.getLogger(__name__)


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


init_log()


def parse_args():
    """
    Parse command line arguments.
    """
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0", help="Host address.")
    parser.add_argument("--port", default=5000, type=int, help="App port.")
    parser.add_argument(
        "--template-folder",
        default="public/template",
        help="Path to the directory with flask templates.",
    )
    parser.add_argument(
        "--static-folder",
        default="public",
        help="Path to the directory with flask static files.",
    )
    parser.add_argument(
        "--debug",
        default=True,
        action="store_true",
        help="Run web server in debug mode.",
    )
    print(__doc__)
    return parser.parse_args()


args = parse_args()

memgraph = Memgraph()
connection_established = False
while(not connection_established):
    try:
        if (memgraph._get_cached_connection().is_active()):
            connection_established = True
    except:
        log.info("Memgraph probably isn't running.")
        time.sleep(4)


app = Flask(
    __name__,
    template_folder=args.template_folder,
    static_folder=args.static_folder,
    static_url_path="",
)


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info(f"Time for {func.__name__} is {duration}")
        return result
    return wrapper


@app.route("/load-data", methods=["GET"])
@log_time
def load_data():
    """Load data into the database."""

    try:
        path = Path("/usr/lib/memgraph/import-data/karate_club.csv")

        memgraph.execute_query(
            f"""LOAD CSV FROM "{path}"
            WITH HEADER DELIMITER " " AS row
            MERGE (a:Member {{id: ToInteger(row.id_1)}})
            MERGE (b:Member {{id: ToInteger(row.id_2)}})
            CREATE (a)-[e:FRIENDS_WITH]->(b);"""
        )
        return Response(status=200)
    except Exception as e:
        log.info("Data loading error.")
        log.info(e)
        return Response(status=500)


@app.route("/get-graph", methods=["GET"])
@log_time
def get_data():
    """Load everything from the database."""
    try:
        results = (
            Match()
            .node("Member", variable="from")
            .to("FRIENDS_WITH")
            .node("Member", variable="to")
            .execute()
        )

        # Set for quickly check if we have already added the node or the edge
        nodes_set = set()
        links_set = set()
        for result in results:
            source_id = result["from"].properties['id']
            target_id = result["to"].properties['id']

            nodes_set.add(source_id)
            nodes_set.add(target_id)

            if (source_id, target_id) not in links_set and (
                target_id,
                source_id,
            ) not in links_set:
                links_set.add((source_id, target_id))

        nodes = [
            {"id": node_id}
            for node_id in nodes_set
        ]
        links = [{"source": n_id, "target": m_id} for (n_id, m_id) in links_set]

        response = {"nodes": nodes, "links": links}

        return Response(json.dumps(response), status=200, mimetype="application/json")
    except Exception as e:
        log.info("Data fetching went wrong.")
        log.info(e)
        return ("", 500)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def main():
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
