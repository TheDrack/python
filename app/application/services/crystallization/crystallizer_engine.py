# -*- coding: utf-8 -*-
import json
import os
import re
import logging
from datetime import datetime

# Configuração de Logs para o console do GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Crystallizer")

class CrystallizerEngine:
    def __init__(self, 
                 cap_path="data/capabilities.json", 
                 crystal_path="data/master_crystal.json", 
                 container_path="app/container.py"):
        
        self.paths = {
            "caps": cap_path,
            "crystal": crystal_path,
            "container": container_path
        }
        
        # Carrega ou Inicializa o Master Crystal
        self.master_crystal = self._load_json(self.paths["crystal"]) or self._init_crystal()
        
        # Carrega as Capabilities (Fonte da Verdade)
        caps_data = self._load_json(self.paths["caps"])
        self.capabilities = caps_data.get('capabilities', []) if caps_data else []

    def _load_json(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao ler JSON em {path}: {str(e)}")
        return None

    def _init_crystal(self):
        return {
            "system_id": "JARVIS_CORE",
            "version": "1.0.0",
            "last_scan": None,
            "crystallization_summary": {
                "total_capabilities": 0,
                "crystallized": 0,
                "connected_legacy": 0,
                "orphan": 0
            },
            "registry": []
        }

    def _map_target(self, cap):
        """Mapeia o destino hexagonal baseado no título e descrição"""
        title = cap.get('title', '').lower()
        desc = cap.get('description', '').lower()
        
        if any(x in title or x in desc for x in ["model", "state", "entity", "schema"]):
            return "app/domain/models/"
        if any(x in title or x in desc for x in ["llm", "ai", "reasoning", "gear", "cognition"]):
            return "app/domain/gears/"
        if any(x in title or x in desc for x in ["adapter", "web", "db", "keyboard", "pyautogui"]):
            return "app/adapters/"
        
        return "app/domain/capabilities/"

    def audit(self):
        """Varre o sistema e identifica a conectividade das capacidades"""
        logger.info("⚡ Iniciando Auditoria do Sistema...")
        
        container_content = ""
        if os.path.exists(self.paths["container"]):
            with open(self.paths["container"], 'r', encoding='utf-8') as f:
                container_content = f.read()

        new_registry = []
        stats = {"total": len(self.capabilities), "crystallized": 0, "legacy": 0, "orphan": 0}

        for cap in self.capabilities:
            cap_id = cap['id']
            notes = cap.get('notes', '')
            
            # Localiza rastro em scripts/
            file_match = re.search(r'(scripts/[\w\.]+\.py)', notes)
            source_file = file_match.group(1) if file_match else "unknown"
            
            # Verifica se está no Container ou se o arquivo de destino já existe
            target_dir = self._map_target(cap)
            target_file_name = f"{cap_id.lower().replace('-', '_')}_core.py"
            target_path = os.path.join(target_dir, target_file_name)
            
            is_in_container = cap_id in container_content
            is_physically_present = os.path.exists(target_path)

            if is_in_container:
                status = "crystallized"
                stats["crystallized"] += 1
            elif source_file != "unknown":
                status = "legacy_connected"
                stats["legacy"] += 1
            else:
                status = "orphan"
                stats["orphan"] += 1

            entry = {
                "id": cap_id,
                "title": cap['title'],
                "status": status,
                "genealogy": {
                    "source": source_file,
                    "target_suggested": target_dir,
                    "target_file": target_path
                },
                "integration": {
                    "in_container": is_in_container,
                    "physically_present": is_physically_present
                },
                "last_check": datetime.now().isoformat()
            }
            new_registry.append(entry)

        self.master_crystal["registry"] = new_registry
        self.master_crystal["last_scan"] = datetime.now().isoformat()
        self.master_crystal["crystallization_summary"] = {
            "total_capabilities": stats["total"],
            "crystallized": stats["crystallized"],
            "connected_legacy": stats["legacy"],
            "orphan": stats["orphan"]
        }
        
        self._save_crystal()
        logger.info(f"✅ Auditoria completa. Total: {stats['total']} | Órfãos: {stats['orphan']}")

    def transmute(self):
        """Cria placeholders físicos para evitar erros de DNA corrompido em missões de evolução"""
        logger.info("🛠 Iniciando Transmutação (Criação de Estrutura)...")
        
        for entry in self.master_crystal["registry"]:
            # Se for órfão ou legado, garantimos que o 'alvo' hexagonal existe para o LLM escrever
            if entry["status"] in ["orphan", "legacy_connected"]:
                target_path = entry["genealogy"]["target_file"]
                target_dir = entry["genealogy"]["target_suggested"]
                
                os.makedirs(target_dir, exist_ok=True)
                
                if not os.path.exists(target_path):
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(f'# -*- coding: utf-8 -*-\n')
                        f.write(f'"""\nCAPABILITY: {entry["title"]}\nID: {entry["id"]}\nSTATUS: Placeholder para Cristalização\n"""\n\n')
                        f.write(f'def init_capability():\n    """Inicializa a lógica desta capacidade"""\n    pass\n')
                    logger.info(f"  [+] Criado Placeholder: {target_path}")

    def _save_crystal(self):
        with open(self.paths["crystal"], 'w', encoding='utf-8') as f:
            json.dump(self.master_crystal, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    engine = CrystallizerEngine()
    engine.audit()      # Fase 1: Mapear
    engine.transmute()  # Fase 2: Criar caminhos para o LLM
