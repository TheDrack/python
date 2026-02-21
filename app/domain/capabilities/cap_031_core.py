
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
    # Lógica para analisar a ação do usuário e entender a intenção
    # Exemplo: se o usuário pede para ligar a luz, a intenção pode ser 'iluminar o ambiente'
    if action == 'ligar_luz':
        return 'iluminar_ambiente'
    elif action == 'desligar_luz':
        return 'economizar_energia'
    else:
        return None
   