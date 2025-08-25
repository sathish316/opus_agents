### Setup 

Install Temporal
$ brew install temporal

Start Temporal Server
$ temporal server start-dev
OR
temporal server start-dev --db-filename your_temporal.db

Install all the dependencies in pyproject.toml
$ uv sync

Activate
$ source .venv/bin/activate

### Run Workers

$ python run_worker.py

### Execute Workflow - Run flask service and submit workflow to Temporal server

$ python run_workflow_starter.py

$ curl -X POST http://localhost:5060/translate \
    -H "Content-Type: application/json" \
        -d '{
        "phrase": "Hello World",
        "language": "french"
    }'