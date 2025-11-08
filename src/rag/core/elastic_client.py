import os
from elasticsearch import Elasticsearch

ES_HOST = os.getenv("ES_HOST", "https://observablt.seetlu.orange-sonatel.com")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")
IS_CI = os.getenv("CI", "false").lower() == "true"

if IS_CI:
    # --- Mode CI/CD : mock du client Elasticsearch ---
    print("🧪 Running in CI mode — Elasticsearch client is mocked.")

    class MockElasticsearch:
        def search(self, *args, **kwargs):
            return {"hits": {"hits": []}}  # renvoie une réponse vide

    es = MockElasticsearch()
else:
    # --- Mode local : vrai client Elasticsearch ---
    if not ES_USERNAME or not ES_PASSWORD:
        print("⚠️  Elasticsearch credentials missing — running without connection.")
        es = None
    else:
        es = Elasticsearch(
            ES_HOST,
            basic_auth=(ES_USERNAME, ES_PASSWORD),
            verify_certs=False,
        )
