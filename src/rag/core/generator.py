import os
from textwrap import dedent
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_augmented_prompt(query: str, incidents: list[dict]) -> str:
    """Construit le prompt enrichi pour le LLM."""

    if not incidents:
        return f"L'utilisateur demande: {query}\nAucun incident trouvé dans la base."

    # On formate les incidents pour le contexte
    context_lines = []
    for inc in incidents:
        when = inc.get("when")
        if when:
            try:
                when = datetime.fromisoformat(when).strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass
        line = f"- [{inc.get('severity', 'N/A')}] {inc.get('site', 'Unknown')} @ {when}: {inc.get('text', '')}"
        context_lines.append(line)

    context_text = "\n".join(context_lines)

    # On combine dans un prompt clair
    prompt = dedent(
        f"""
    Tu es un assistant d'exploitation réseau. Résume et explique les incidents ci-dessous.

    CONTEXTE:
    {context_text}

    QUESTION:
    {query}

    INSTRUCTION:
    - Réponds en français.
    - Sois factuel et concis.
    - Si plusieurs sites sont mentionnés, regroupe-les.
    - Indique les sévérités et zones impactées.
    - Ne génère rien qui n'existe pas dans le contexte.
    """
    )

    return prompt


def generate_answer(query: str, incidents: list[dict]) -> str:
    """Appelle le LLM pour produire la réponse finale."""
    prompt = build_augmented_prompt(query, incidents)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant expert en supervision réseau.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        # Fallback si l'appel LLM échoue
        return f"(⚠️ Fallback) Impossible d'appeler le modèle. Voici le résumé brut:\n\n{prompt}"
