import requests
from datetime import datetime
from textwrap import dedent


def build_augmented_prompt(query: str, incidents: list[dict]) -> str:
    """Construit le prompt enrichi pour le modèle Ollama local."""
    if not incidents:
        return f"L'utilisateur demande: {query}\nAucun incident trouvé dans la base."

    context_lines = []
    for inc in incidents:
        when = inc.get("when")
        if when:
            try:
                when = datetime.fromisoformat(when).strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass

        line = (
            f"- [{inc.get('severity', 'N/A')}] "
            f"{inc.get('site', 'Unknown')} @ {when}: {inc.get('text', '')}"
        )
        context_lines.append(line)

    context_text = "\n".join(context_lines)

    prompt = dedent(
        f"""
    Tu es un assistant d'exploitation réseau.
    Utilise UNIQUEMENT les informations ci-dessous pour répondre.

    CONTEXTE:
    {context_text}

    QUESTION:
    {query}

    INSTRUCTION:
    - Réponds en français, clair et concis.
    - Ne crée aucune information absente du contexte.
    - Regroupe les incidents similaires.
    - Indique les sévérités et zones affectées.
    """
    )

    return prompt


def generate_answer(query: str, incidents: list[dict], model: str = "llama3") -> str:
    """Appelle Ollama localement pour produire une réponse."""
    prompt = build_augmented_prompt(query, incidents)

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un expert réseau et supervision.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
            },
            timeout=60,
        )

        if response.status_code == 200:
            data = response.json()
            return data["message"]["content"].strip()
        else:
            return f"(⚠️ Ollama Error {response.status_code}) {response.text}"

    except Exception as e:
        return f"(⚠️ Erreur locale) Impossible d'appeler Ollama : {e}"
