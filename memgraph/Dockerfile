FROM memgraph/memgraph-mage:1.1-dev

USER root

# Install pip packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the local query modules and data import files
COPY transformations/ /usr/lib/memgraph/query_modules
COPY import-data/friendship_network.csv /usr/lib/memgraph/import-data/friendship_network.csv

USER memgraph
