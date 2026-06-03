"""
Script de test standalone — valide que ClaudeProvider fonctionne.
Pas besoin de FastAPI, appel direct au provider.

Usage :
    cp .env.example .env   # puis renseigner ANTHROPIC_API_KEY
    python test_extraction.py
"""

import json
import sys
import io

# Force UTF-8 sur la console Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from pathlib import Path
from dotenv import load_dotenv
from providers.claude_provider import ClaudeProvider

load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

# Document fictif simulant un rapport financier PDF extrait en texte brut
DOCUMENT = """
RAPPORT FINANCIER ANNUEL 2023
Société : TechVision SAS
SIRET : 812 345 678 00021
Siège social : 14 rue de la République, 69001 Lyon

1. Résultats financiers
Le chiffre d'affaires annuel s'élève à 2.3M€ en progression de 18% par rapport à 2022.
La marge brute atteint 67% contre 61% l'année précédente.

2. Effectifs
L'entreprise compte 34 collaborateurs au 31 décembre 2023, dont 12 ingénieurs
recrutés au cours de l'exercice.

3. Perspectives
Le carnet de commandes au 1er janvier 2024 représente 1.1M€, assurant
une visibilité de 6 mois sur l'activité.

Fait à Lyon, le 15 mars 2024
Directeur Général : Marc Dupont
"""

FIELDS = ["chiffre_affaires", "marge_brute", "nombre_employes", "carnet_de_commandes", "dirigeant"]


def test_extraction():
    print("=" * 60)
    print("TEST — Extraction structurée avec Claude")
    print("=" * 60)

    provider = ClaudeProvider()

    print(f"\n→ Champs demandés : {FIELDS}\n")
    print("→ Appel Claude en cours...\n")

    result = provider.extract_structured_data(DOCUMENT, FIELDS)

    print("✅ Résultat :\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("TEST — Génération rapport en streaming")
    print("=" * 60)
    print("\n→ Streaming en cours...\n")

    for chunk in provider.generate_report_stream(result):
        print(chunk, end="", flush=True)

    print("\n\n✅ Streaming terminé")


if __name__ == "__main__":
    try:
        test_extraction()
    except Exception as e:
        print(f"\n❌ Erreur : {e}", file=sys.stderr)
        sys.exit(1)
