from rag.core.generator import generate_answer


def test_summarize_incidents_empty_list():
    """Si la liste d'incidents est vide, la fonction doit renvoyer un texte informatif."""
    query = "Incident RN7"
    incidents = []

    result = generate_answer(query, incidents)

    assert isinstance(result, str)
    assert len(result.strip()) > 0  # le modèle a bien produit quelque chose


def test_summarize_incidents_valid_input():
    """Avec des incidents, on vérifie que la fonction renvoie bien un résumé texte."""
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
    assert len(result.strip()) > 0
    keywords = ["incident", "kedougou", "rn7", "link", "down", "alert"]
    assert any(k in result.lower() for k in keywords)
