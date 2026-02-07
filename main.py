import os
import uvicorn
from app.adapters.infrastructure.api_server import create_api_server
from app.application.services import AssistantService

def start_cloud():
    """Inicializa o Jarvis em modo API para o Render/Nuvem"""
    # Inicializa o serviço principal
    assistant_service = AssistantService() 
    # Cria o servidor usando a Factory que você já tem
    app = create_api_server(assistant_service)
    
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Jarvis Online na Nuvem - Porta {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Se houver uma porta definida, estamos no Render (Cloud)
    if os.getenv("PORT"):
        start_cloud()
    else:
        # Se não, roda o modo voz local que você já tinha
        from app.bootstrap_edge import main
        main()
