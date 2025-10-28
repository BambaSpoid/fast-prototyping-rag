from datetime import datetime


def summarize_incidents(query: str, incidents: list[dict]) -> str:
    """
    incidents: liste de dicts venant de search_bm25()
    chaque dict ressemble à:
    {
        "score": ...,
        "when": "2025-07-02T23:07:44",
        "site": "SITE-RN7-L",
        "severity": "Major",
        "text": "S1ap Link Down | ... Kedougou"
    }
    """

    if not incidents:
        return f"Aucun incident trouvé pour: {query}"

    lines = []
    lines.append(f"Résumé pour: {query}")
    lines.append(f"Nombre d'incidents trouvés: {len(incidents)}")
    lines.append("")

    for idx, inc in enumerate(incidents, start=1):
        # lisibilité de la date
        when_human = inc["when"]
        if when_human:
            try:
                dt = datetime.fromisoformat(when_human)
                when_human = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass

        line = (
            f"{idx}. "
            f"[{inc.get('severity', 'N/A')}] "
            f"{inc.get('site', 'Unknown site')} "
            f"@ {when_human} "
            f"-> {inc.get('text', '')}"
        )
        lines.append(line)

    return "\n".join(lines)
