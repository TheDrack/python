# -*- coding: utf-8 -*-
import argparse
import os
import sys
import json
import re
from pathlib import Path
from app.application.services.metabolism_core import MetabolismCore

def clean_json_response(raw_response):
    if isinstance(raw_response, dict):
        return raw_response
    clean_text = re.sub(r'```(?:json)?\n?(.*?)\n?```', r'\1', raw_response, flags=re.DOTALL)
    clean_text = clean_text.strip()
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        match = re.search(r'(\{.*\})', clean_text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise ValueError(f"Falha ao parsear JSON da IA: {raw_response[:100]}")

def get_target_from_crystal(cap_id: str, crystal_path="data/master_crystal.json"):
    """Consulta o Master Crystal para encontrar o caminho físico criado pelo Crystallizer."""
    path = Path(crystal_path)
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        crystal = json.load(f)
    for entry in crystal.get("registry", []):
        if entry["id"] == cap_id:
            return entry["genealogy"]["target_file"]
    return None

def evolve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', required=True)
    parser.add_argument('--intent', required=True)
    parser.add_argument('--impact', required=True)
    parser.add_argument('--roadmap-context', default="")
    args = parser.parse_args()

    core = MetabolismCore()
    issue_body = os.getenv('ISSUE_BODY', '')
    
    # Extração do ID da Capability (ex: CAP-024)
    cap_id_match = re.search(r'(CAP-\d+)', issue_body)
    if not cap_id_match:
        print("❌ Erro: ID da capability (CAP-XXX) não encontrado no ISSUE_BODY.")
        sys.exit(1)
    
    cap_id = cap_id_match.group(1)

    # --- PASSO 1: LOCALIZAÇÃO ---
    print(f"🔍 Buscando coordenadas para {cap_id} no Master Crystal...")
    target_file = get_target_from_crystal(cap_id)
    
    if not target_file:
        print(f"❌ Erro: {cap_id} não foi cristalizado previamente.")
        sys.exit(1)

    path = Path(target_file)
    current_code = path.read_text(encoding='utf-8') if path.exists() else ""

    # --- PASSO 2: ENGENHARIA DE CÓDIGO ---
    system_prompt = (
        "Você é o Engenheiro Senior do JARVIS. Implemente a lógica completa para a Capability.\n"
        f"Arquivo alvo: {target_file}\n"
        "Responda APENAS um JSON: {\"code\": \"...\", \"summary\": \"...\"}"
    )
    user_prompt = f"MISSÃO: {issue_body}\nCONTEXTO: {args.roadmap_context}\nCÓDIGO BASE:\n{current_code}"

    try:
        print(f"🧬 Iniciando mutação em: {target_file}")
        response = core.ask_jarvis(system_prompt, user_prompt)
        mutation = clean_json_response(response)

        new_code = mutation.get('code', '')
        if len(new_code.strip()) > 50:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(new_code, encoding='utf-8')
            print(f"✅ Mutação finalizada: {mutation.get('summary')}")
        else:
            print("❌ Erro: Código gerado insuficiente.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Falha no ciclo de evolução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    evolve()
