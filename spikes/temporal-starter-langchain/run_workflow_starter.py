import asyncio
import uuid

from flask import Flask, jsonify, request, abort
from temporalio.client import Client

from shared import TASK_QUEUE_NAME, TranslateInput
from workflow import TranslateWorkflow, TranslateSuperWorkflow

def create_app(temporal_client: Client):
    app = Flask(__name__)

    @app.route("/translate", methods=["POST"])
    async def translate():
        """
        Endpoint to translate a phrase.

        Returns:
            Response: JSON response with translated phrase or error message.
        """
        try:
            phrase = request.json.get("phrase")
            language = request.json.get("language")

            input_data = TranslateInput(
                phrase=phrase,
                language=language,
            )
            print(f"Translating phrase: {phrase} to {language}")

            result = await temporal_client.execute_workflow(
                TranslateWorkflow.run,
                input_data,
                id=f"langchain-translation-{uuid.uuid4()}",
                task_queue=TASK_QUEUE_NAME,
            )
        except Exception as e:
            abort(500, description=str(e))

        return jsonify({
                "translation": result,
        })

    return app

async def main():
    temporal_client = await Client.connect("localhost:7233")
    app = create_app(temporal_client)
    app.run(host="0.0.0.0", port=5060, debug=True)

if __name__ == "__main__":
    asyncio.run(main())