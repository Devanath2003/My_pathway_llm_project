import os
import pathway as pw
from model_wrappers import SentenceTransformerTask


HTTP_HOST = os.environ.get("EMBEDDER_REST_CONNECTOR_HOST", "127.0.0.1")
HTTP_PORT = os.environ.get("EMBEDDER_REST_CONNECTOR_PORT", "8880")
EMBEDDER_LOCATOR = os.environ.get(
    "EMBEDDER_LOCATOR", "sentence-transformers/all-MiniLM-L6-v2"
)


class InputSchema(pw.Schema):
    text: str


def run():
    document, response_writer = pw.io.http.rest_connector(
        host=HTTP_HOST,
        port=int(HTTP_PORT),
        schema=InputSchema,
        autocommit_duration_ms=50,
    )

    embedder = SentenceTransformerTask(model=EMBEDDER_LOCATOR)

    embedding = document.select(result=embedder.apply(text=pw.this.text))

    response_writer(embedding)

    pw.run()


if __name__ == "__main__":
    run()