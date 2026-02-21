# -*- coding: utf-8 -*-
import argparse
import os
import sys
import json
import re
from pathlib import Path
from app.application.services.metabolism_core import MetabolismCore

def extract_code_manually(text):
    """Tenta extrair o código mesmo se a IA falhar no JSON puro."""
    # Busca por blocos de código python
    code_match = re.search(r'```python\n(.*?)\n```', text, re.DOTALL)
    if not code_match:
        # Busca por qualquer bloco de código
        code_match = re.search(r'```\n(.*?)\n```', text, re.DOTALL)
    
    if code_match:
        return code_match.group(1)
    return text

def clean_json_response(raw_response):
    if isinstance(raw_response, dict): return raw_response
    try:
        # Limpeza de markdown
        clean_text = re.sub(r'```(?:json)?\n?(.*?)\n?```', r'\1', raw_response, flags=re.DOTALL).strip()
        return json.loads(clean_text)
    except:
        # Se falhar, tenta capturar apenas o objeto JSON
        match = re.search(r'(\{.*\})', raw_response, re.DOTALL)
        if match:
            try: return json.loads(match.group(1))
            except: pass
        # Fallback: Se não é JSON, assume que a resposta é o próprio código (comum em falhas de prompt)
        return {"code": extract_code_manually(raw_response), "summary": "Fallback extraction"}

def get_entry_from_crystal(cap_id: str, crystal_path="data/master_crystal.json"):
    path = Path(crystal_path)
    if not path.exists(): return None
    with open(path, 'r', encoding='utf-8') as f:
        crystal = json.load(f)
    for entry in crystal.get("registry", []):
        if entry["id"] == cap_id: return entry
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
    match = re.search(r'(CAP-\d+)', issue_body)
    if not match: sys.exit(1)
    
    cap_id = match.group(1)
    entry = get_entry_from_crystal(cap_id)
    if not entry: sys.exit(1)

    target_file = Path(entry["genealogy"]["target_file"])
    
    # Prompt de Força Bruta
    system_prompt = (
        f"Você é o motor de evolução do JARVIS. Implemente a lógica da {cap_id}.\n"
        "RESPONDA APENAS O CÓDIGO DENTRO DE UM JSON.\n"
        "O código deve ter: def execute(context=None):"
    )
    user_prompt = f"ISSUE: {issue_body}\nARQUIVO: {target_file}"

    try:
        print(f"🧬 Evoluindo {cap_id}...")
        response = core.ask_jarvis(system_prompt, user_prompt)
        mutation = clean_json_response(response)
        new_code = mutation.get('code', '')

        # Se o código extraído for muito curto ou inválido, tentamos o fallback no texto bruto
        if "def execute" not in new_code:
            new_code = extract_code_manually(response)

        if "def execute" in new_code:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(new_code, encoding='utf-8')
            print(f"✅ Sucesso: {target_file}")
        else:
            print("❌ Falha crítica: Estrutura 'execute' não encontrada na resposta.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    evolve()
