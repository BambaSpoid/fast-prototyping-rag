import pytest
from rag.core.generator import summarize_incidents


def test_summarize_incidents_empty_list():
    query = "Incident RN7"
    incidents = []
    result = summarize_incidents(query, incidents)

    assert isinstance(result, str)
    assert "Aucun incident trouvé" in result


def test_summarize_incidents_valid_input():
    query = "Incident RN7"
    incidents = [
        {
            "score": 12.0,
            "when": "2025-07-02T23:07:44",
            "site": "SITE-RN7-L",
            "severity": "Major",
            "text": "S1ap Link Down | Incident à Kedougou",
        },
        {
            "score": 8.5,
            "when": "2025-07-03T14:12:00",
            "site": "SITE-RN7-R",
            "severity": "Minor",
            "text": "Déconnexion intermittente | Tambacounda",
        },
    ]

    result = summarize_incidents(query, incidents)

    assert isinstance(result, str)
    assert "Résumé pour" in result
    assert "SITE-RN7-L" in result
    assert "Kedougou" in result
    assert "2025-07-02 23:07:44" in result
    assert result.count("\n") >= 3
