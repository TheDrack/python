
def execute(context=None):
    if context is None:
        context = {}
    
    # Carregar histórico de interações do usuário
    user_history = load_user_history(context['user_id'])
    
    # Identificar padrões de interação atuais
    current_patterns = identify_current_patterns(user_history)
    
    # Detectar mudanças nos padrões de interação
    changes = detect_changes(current_patterns, user_history)
    
    # Atualizar conhecimento do sistema sobre o usuário
    update_user_knowledge(changes, context['user_id'])
    
    return changes
   