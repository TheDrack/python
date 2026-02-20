# -*- coding: utf-8 -*-
import os
import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("Mutator")


class MetabolismMutator:
    def __init__(self, repo_path=None):
        self.repo_path = Path(repo_path) if repo_path else Path(os.getcwd())
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def apply_mutation(
        self,
        strategy: str,
        intent: str,
        capability_id: int,
        capability_name: str,
        context: str,
    ):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            logger.error("GROQ_API_KEY não encontrada.")
            return {"success": False}

        try:
            import requests
        except ImportError:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import requests

        # ==================================================
        # PASSO 1 — ANÁLISE ARQUITETURAL
        # ==================================================
        analysis_prompt = f"""
Você está evoluindo um sistema chamado JARVIS.

CAPABILITY_ID: {capability_id}
CAPABILITY_NAME: {capability_name}

CONTEXTO ATUAL:
{context}

OBJETIVO:
Decidir qual arquivo deve ser criado ou modificado para IMPLEMENTAR
ESSA CAPABILITY.

DIRETRIZES DE ARQUITETURA:
- Serviços: app/application/services/
- Infraestrutura: app/adapters/infrastructure/
- Scripts: scripts/
- NÃO criar arquivos desnecessários
- Evolução mínima e segura

RETORNE JSON PURO:
{{
  "target_file": "<caminho>",
  "action": "create|modify",
  "reason": "<motivo técnico>"
}}
"""

        try:
            resp_analysis = requests.post(
                self.groq_url,
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "Arquiteto Senior. Responda APENAS JSON."},
                        {"role": "user", "content": analysis_prompt},
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.1,
                },
                timeout=30,
            )

            if resp_analysis.status_code != 200:
                logger.error(f"Erro API Arquitetura: {resp_analysis.text}")
                return {"success": False}

            analysis_data = json.loads(
                resp_analysis.json()["choices"][0]["message"]["content"]
            )

            target_file = analysis_data["target_file"]
            logger.info(f"🎯 Arquivo alvo: {target_file}")

            path = self.repo_path / target_file
            path.parent.mkdir(parents=True, exist_ok=True)
            current_code = (
                path.read_text(encoding="utf-8")
                if path.exists()
                else "# Novo arquivo JARVIS\n"
            )

            # ==================================================
            # PASSO 2 — ENGENHARIA (MUTAÇÃO)
            # ==================================================
            mutation_prompt = f"""
CAPABILITY_ID: {capability_id}
CAPABILITY_NAME: {capability_name}
STRATEGY: {strategy}

ARQUIVO: {target_file}

CÓDIGO ATUAL:
{current_code}

REQUISITOS:
- Implementar a capability declarada
- Preservar compatibilidade arquitetural
- Código completo (arquivo inteiro)
- Sem comentários desnecessários

RETORNE JSON PURO:
{{
  "code": "<arquivo completo>",
  "summary": "<resumo técnico da mutação>"
}}
"""

            resp_mutation = requests.post(
                self.groq_url,
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Engenheiro Senior. Retorne APENAS JSON válido.",
                        },
                        {"role": "user", "content": mutation_prompt},
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.1,
                },
                timeout=60,
            )

            if resp_mutation.status_code != 200:
                logger.error(f"Erro API Engenharia: {resp_mutation.text}")
                return {"success": False}

            content = json.loads(
                resp_mutation.json()["choices"][0]["message"]["content"]
            )

            new_code = content.get("code", "").strip()
            summary = content.get("summary", "")

            if not new_code or len(new_code) < 20:
                logger.error("Código retornado inválido ou vazio.")
                return {"success": False}

            # ==================================================
            # PASSO 3 — APLICAÇÃO + SUMMARY
            # ==================================================
            path.write_text(new_code, encoding="utf-8")

            summary_text = f"""
Capability ID: {capability_id}
Capability Name: {capability_name}
Strategy: {strategy}
File Modified: {target_file}
Timestamp: {datetime.utcnow().isoformat()}

Resumo:
{summary}
""".strip()

            (self.repo_path / "mutation_summary.txt").write_text(
                summary_text, encoding="utf-8"
            )

            logger.info(f"✅ Capability {capability_id} mutada com sucesso.")
            return {"success": True}

        except Exception as e:
            logger.error(f"❌ Falha crítica na mutação: {e}")
            return {"success": False}


# ==================================================
# ENTRYPOINT
# ==================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--strategy", required=True)
    parser.add_argument("--intent", required=True)

    parser.add_argument("--capability-id", required=True, type=int)
    parser.add_argument("--capability-name", required=True)

    parser.add_argument("--context", required=True)

    args = parser.parse_args()

    mutator = MetabolismMutator()
    result = mutator.apply_mutation(
        strategy=args.strategy,
        intent=args.intent,
        capability_id=args.capability_id,
        capability_name=args.capability_name,
        context=args.context,
    )

    sys.exit(0 if result.get("success") else 1)