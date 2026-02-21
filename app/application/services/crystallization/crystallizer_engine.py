# -*- coding: utf-8 -*-
import json
import os
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Configuração de Logs
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
            "caps": Path(cap_path),
            "crystal": Path(crystal_path),
            "container": Path(container_path)
        }
        
        # Garante pastas base
        self.paths["caps"].parent.mkdir(parents=True, exist_ok=True)
        
        # Carrega Master Crystal ou inicia novo
        self.master_crystal = self._load_json(self.paths["crystal"]) or self._init_crystal()
        
        # Carrega Capabilities
        caps_data = self._load_json(self.paths["caps"])
        self.capabilities = caps_data.get('capabilities', []) if caps_data else []

    def _load_json(self, path: Path):
        try:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao ler JSON em {path}: {str(e)}")
        return None

    def _init_crystal(self):
        return {
            "system_id": "JARVIS_CORE",
            "version": "1.1.0",
            "last_scan": None,
            "registry": []
        }

    def _map_target(self, cap: Dict[str, Any]) -> str:
        title = cap.get('title', '').lower()
        desc = cap.get('description', '').lower()
        
        if any(x in title or x in desc for x in ["llm", "ai", "gear", "cognition", "groq"]):
            return "app/domain/gears/"
        if any(x in title or x in desc for x in ["model", "state", "entity", "schema"]):
            return "app/domain/models/"
        if any(x in title or x in desc for x in ["adapter", "web", "pyautogui", "os", "keyboard"]):
            return "app/adapters/"
        
        return "app/domain/capabilities/"

    def audit(self):
        """Fase 1: Mapear integridade (JSON + Pasta + Container)"""
        logger.info("⚡ Auditoria: Validando Tríade de Cristalização...")
        
        container_content = ""
        if self.paths["container"].exists():
            container_content = self.paths["container"].read_text(encoding='utf-8')

        new_registry = []
        for cap in self.capabilities:
            cap_id = cap['id']
            target_dir = self._map_target(cap)
            target_file = f"{cap_id.lower().replace('-', '_')}_core.py"
            target_path = os.path.join(target_dir, target_file)
            
            # Validação dos 3 Pilares
            is_in_container = f'"{cap_id}"' in container_content
            is_physically_present = Path(target_path).exists()

            status = "crystallized" if is_in_container and is_physically_present else "incomplete"

            new_registry.append({
                "id": cap_id,
                "title": cap['title'],
                "status": status,
                "genealogy": {
                    "target_suggested": target_dir,
                    "target_file": target_path
                },
                "integration": {
                    "in_container": is_in_container,
                    "physically_present": is_physically_present
                }
            })

        self.master_crystal["registry"] = new_registry
        self.master_crystal["last_scan"] = datetime.now().isoformat()
        self._save_crystal()

    def transmute(self):
        """Fase 2: Criar caminhos físicos (Arquiteto)"""
        logger.info("🛠️ Transmutação: Criando estrutura física...")
        
        for entry in self.master_crystal["registry"]:
            if not entry["integration"]["physically_present"]:
                t_path = Path(entry["genealogy"]["target_file"])
                t_dir = Path(entry["genealogy"]["target_suggested"])
                
                t_dir.mkdir(parents=True, exist_ok=True)
                (t_dir / "__init__.py").touch()

                with open(t_path, 'w', encoding='utf-8') as f:
                    f.write(f'# -*- coding: utf-8 -*-\n"""CAPABILITY: {entry["title"]}\nID: {entry["id"]}"""\n\ndef execute(context=None):\n    return {{"status": "initialized", "id": "{entry["id"]}"}}\n')
                
                logger.info(f"  [💎] Placeholder criado: {t_path}")
                entry["integration"]["physically_present"] = True

    def stitch(self):
        """Fase 3: Ligar ao Container (Costureiro)"""
        logger.info("🧵 Stitching: Conectando capacidades ao Container...")
        
        if not self.paths["container"].exists():
            logger.error("Container não encontrado para costura.")
            return

        content = self.paths["container"].read_text(encoding='utf-8')
        modified = False

        for entry in self.master_crystal["registry"]:
            if entry["integration"]["physically_present"] and not entry["integration"]["in_container"]:
                cap_id = entry["id"]
                var_name = f"{cap_id.lower().replace('-', '_')}_exec"
                
                # 1. Gerar Import Path (ex: from app.domain.gears.x_core import execute)
                raw_path = entry["genealogy"]["target_file"].replace('.py', '').replace('/', '.').replace('\\', '.')
                import_stmt = f"from {raw_path} import execute as {var_name}"
                
                if import_stmt not in content:
                    # Inserção inteligente: após o último import existente
                    content = re.sub(r'(from app\..*import .*)', r'\1\n' + import_stmt, content, count=1)
                
                # 2. Inserção no Dicionário self.capabilities
                mapping = f'            "{cap_id}": {var_name},'
                if f'"{cap_id}"' not in content:
                    content = re.sub(r'(self\.capabilities = \{)', r'\1\n' + mapping, content)
                    logger.info(f"  [🧵] {cap_id} costurado ao Container.")
                    modified = True
                    entry["integration"]["in_container"] = True
                    entry["status"] = "crystallized"

        if modified:
            self.paths["container"].write_text(content, encoding='utf-8')
            self._save_crystal()

    def _save_crystal(self):
        with open(self.paths["crystal"], 'w', encoding='utf-8') as f:
            json.dump(self.master_crystal, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    engine = CrystallizerEngine()
    engine.audit()      # Mapeia
    engine.transmute()  # Cria arquivos
    engine.stitch()     # Conecta no Container
    logger.info("✨ JARVIS Cristalizado e Integrado.")
