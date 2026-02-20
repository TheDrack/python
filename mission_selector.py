
import sys

import json

from typing import List, Dict



class MissionSelector:

    def __init__(self, objectives: List[Dict]):

        self.objectives = objectives

        self.sorted_objectives = self.sort_by_systemic_impact()

    

    def sort_by_systemic_impact(self) -> List[Dict]:

        # Implementação da lógica de ordenação por impacto sistêmico

        return sorted(self.objectives, key=lambda x: x['systemic_impact'], reverse=True)

    

    def get_sorted_objectives(self) -> List[Dict]:

        return self.sorted_objectives



# Exemplo de uso:

objectives = [

    {'name': 'Objetivo 1', 'systemic_impact': 5},

    {'name': 'Objetivo 2', 'systemic_impact': 3},

    {'name': 'Objetivo 3', 'systemic_impact': 8}

]



mission_selector = MissionSelector(objectives)

sorted_objectives = mission_selector.get_sorted_objectives()



for objective in sorted_objectives:

    print(objective['name'], objective['systemic_impact'])

