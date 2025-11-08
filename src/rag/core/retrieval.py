import os
from .elastic_client import es

INDEX = os.getenv("ES_INDEX", "metrics-cdr-alarmesu2020-bigdata")


def search_bm25(query: str, k: int = 5):
    """
    Recherche les incidents les plus pertinents avec BM25.
    Tolère l'absence de connexion Elasticsearch (CI, local sans credentials).
    """

    # Si le client Elasticsearch n'est pas initialisé (mode CI ou offline)
    if es is None:
        print("⚠️  Elasticsearch client is None — returning empty results.")
        return []

    try:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "addtional_text^3",
                        "IncidentName^2",
                        "alarmname",
                        "business_affected",
                        "locationinformation",
                        "enrich_nomsite",
                        "enrich_region",
                    ],
                    "type": "best_fields",
                }
            },
            "_source": [
                "addtional_text",
                "IncidentName",
                "alarmname",
                "business_affected",
                "locationinformation",
                "enrich_nomsite",
                "enrich_region",
                "@timestamp",
                "eNodeB_name",
                "severity",
            ],
            "size": k,
        }

        hits = es.search(index=INDEX, body=body)["hits"]["hits"]

        results = []
        for h in hits:
            src = h["_source"]

            text_parts = [
                src.get("IncidentName"),
                src.get("alarmname"),
                src.get("addtional_text"),
                src.get("business_affected"),
                src.get("locationinformation"),
                src.get("enrich_nomsite"),
                src.get("enrich_region"),
            ]
            summary = " | ".join([p for p in text_parts if p])

            results.append(
                {
                    "score": h["_score"],
                    "when": src.get("@timestamp"),
                    "site": src.get("eNodeB_name"),
                    "severity": src.get("severity"),
                    "text": summary,
                }
            )

        return results

    except Exception as e:
        print(f"❌ Elasticsearch error during search: {e}")
        return []
