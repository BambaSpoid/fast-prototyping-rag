from .elastic_client import es
import os

INDEX = os.getenv("ES_INDEX", "metrics-cdr-alarmesu2020-bigdata")


def search_bm25(query: str, k: int = 5):
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

        # On fabrique un petit résumé lisible pour l'UI
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
