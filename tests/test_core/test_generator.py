from rag.core.generator import generate_answer


def test_summarize_incidents_empty_list():
    query = "Incident RN7"
    incidents = []
    result = generate_answer(query, incidents)

    assert isinstance(result, str)
    assert "pas d'incidents" in result.lower()


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

    result = generate_answer(query, incidents)

    assert isinstance(result, str)
    assert "SITE-RN7-L" in result
    assert "Kedougou" in result
    assert "2025-07-02" in result
