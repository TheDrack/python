import os
import uvicorn
from app.adapters.infrastructure.api_server import create_api_server

# Tenta importar o DependencyManager se ele existir
try:
    from app.application.services import DependencyManager
    HAS_MANAGER = True
except ImportError:
    from app.application.services import AssistantService
    HAS_MANAGER = False

def start_cloud():
    """Inicializa o Jarvis em modo API para o Render/Nuvem"""
    
    if HAS_MANAGER:
        # Se tivermos o gestor, ele resolve as 5 dependências sozinho
        manager = DependencyManager()
        assistant_service = manager.get_assistant_service()
    else:
        # Se não houver manager, precisamos de ver como o bootstrap_edge.py 
        # instancia o AssistantService e replicar aqui. 
        # Por agora, tentamos a importação direta se o seu Service tiver defaults:
        from app.application.services import AssistantService
        # Nota: Se isto falhar, precisaremos de copiar a lógica de montagem do bootstrap_edge
        assistant_service = AssistantService() 

    app = create_api_server(assistant_service)
    
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Jarvis Online na Nuvem - Porta {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    if os.getenv("PORT"):
        start_cloud()
    else:
        from app.bootstrap_edge import main
        main()
