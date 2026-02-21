import json
import os
import re
import logging
from datetime import datetime

logger = logging.getLogger("Crystallizer")
logging.basicConfig(level=logging.INFO)

class CrystallizerEngine:
    def __init__(self):
        self.paths = {
            "caps": "data/capabilities.json",
            "crystal": "data/master_crystal.json",
            "container": "app/container.py"
        }
        self.master_crystal = self._load_json(self.paths["crystal"]) or self._init_crystal()
        self.capabilities = self._load_json(self.paths["caps"]).get("capabilities", [])

    def _load_json(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            return None
        return None

    def _init_crystal(self):
        return {"system_id": "JARVIS_CORE", "last_scan": None, "registry": []}

    def audit(self):
        logger.info("⚡ Iniciando Auditoria de Cristalização...")
        with open(self.paths["container"], 'r') as f:
            container_content = f.read()

        new_registry = []
        for cap in self.capabilities:
            cap_id = cap['id']
            # Busca rastro nos códigos soltos (scripts/)
            notes = cap.get('notes', '')
            is_orphan = "scripts/" in notes
            
            # Checa se já está no sistema nervoso
            is_connected = cap_id in container_content or cap['title'].split()[0] in container_content

            entry = {
                "id": cap_id,
                "title": cap['title'],
                "status": "crystallized" if is_connected else "legacy_connected" if is_orphan else "orphan",
                "original_home": re.search(r'scripts/[\w\.]+', notes).group(0) if is_orphan else "unknown",
                "target_hexagonal": self._map_target(cap),
                "last_check": datetime.now().isoformat()
            }
            new_registry.append(entry)

        self.master_crystal["registry"] = new_registry
        self.master_crystal["last_scan"] = datetime.now().isoformat()
        
        with open(self.paths["crystal"], 'w') as f:
            json.dump(self.master_crystal, f, indent=4)
        logger.info("✅ Master Crystal Atualizado.")

    def _map_target(self, cap):
        title = cap['title'].lower()
        if "model" in title or "state" in title: return "app/domain/models/"
        if "llm" in title or "ai" in title: return "app/domain/gears/"
        if "adapter" in title or "detect" in title: return "app/adapters/"
        return "app/domain/capabilities/"

if __name__ == "__main__":
    CrystallizerEngine().audit()
