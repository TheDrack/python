
def execute(context=None):
    if context is None:
        context = {}
    user_actions = context.get('user_actions', [])
    goals = []
    for action in user_actions:
        intent = analyze_action(action)
        if intent:
            goals.append(intent)
    return goals

def analyze_action(action):
    # Lógica para analisar a ação e identificar a intenção
    # Exemplo: se a ação for 'abrir porta', a intenção pode ser 'entrar'
    intentions = {
        'abrir porta': 'entrar',
        'fechar porta': 'sair'
    }
    return intentions.get(action, None)
