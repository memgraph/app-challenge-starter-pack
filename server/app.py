import database
import json
import logging
import os
import time
from argparse import ArgumentParser
from flask import Flask, Response, render_template
from functools import wraps


KAFKA_HOST = os.getenv("KAFKA_HOST", "kafka")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "memgraph-mage")
MEMGRAPH_PORT = int(os.getenv("MEMGRAPH_PORT", "7687"))
PATH_TO_INPUT_FILE = os.getenv("PATH_TO_INPUT_FILE", "/")


log = logging.getLogger(__name__)


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


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

memgraph = None


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
        memgraph.load_data_into_memgraph(PATH_TO_INPUT_FILE)
        return Response(status=200)
    except Exception as e:
        log.info(f"Data loading error: {e}")
        return Response(status=500)


@app.route("/get-graph", methods=["GET"])
@log_time
def get_data():
    """Load everything from the database."""
    try:
        results = memgraph.get_graph()

        # Set for quickly check if we have already added the node or the edge
        nodes_set = set()
        links_set = set()
        for result in results:
            source_id = result["from"].properties['id']
            target_id = result["to"].properties['id']

            nodes_set.add(source_id)
            nodes_set.add(target_id)

            if ((source_id, target_id) not in links_set and
                    (target_id, source_id,) not in links_set):
                links_set.add((source_id, target_id))

        nodes = [
            {"id": node_id}
            for node_id in nodes_set
        ]
        links = [{"source": n_id, "target": m_id} for (n_id, m_id) in links_set]

        response = {"nodes": nodes, "links": links}
        return Response(json.dumps(response), status=200, mimetype="application/json")
    except Exception as e:
        log.info(f"Data loading error: {e}")
        return ("", 500)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def main():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_log()
        global memgraph
        memgraph = database.Memgraph(MEMGRAPH_HOST,
                                     MEMGRAPH_PORT)
    app.run(host=args.host,
            port=args.port,
            debug=args.debug)


if __name__ == "__main__":
    main()
