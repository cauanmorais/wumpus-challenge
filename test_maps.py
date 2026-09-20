
MAPAS_TESTE = {
    '1': {
        'nome': "Caminho Aberto (Fácil)",
        'size': 4,
        'gold': (4, 4),
        'wumpus': (4, 1),
        'pits': [(3, 1), (4, 2)]
    },
    '2': {
        'nome': "Wumpus Bloqueando o Caminho (Médio)",
        'size': 4,
        'gold': (4, 1),
        'wumpus': (2, 4), # O robô provavelmente terá que atirar para passar
        'pits': [(1, 3), (1, 2)]
    },
    '3': {
        'nome': "Corredor da Morte (Difícil)",
        'size': 4,
        'gold': (4, 1),
        'wumpus': (4, 4),
        'pits': [(2, 1), (2, 2)] # Cria um gargalo perigoso
    },
    '4': {
            'nome': "Mapa teste da aula (Difícil)",
            'size': 4,
            'gold': (4, 1),
            'wumpus': (3, 4),
            'pits': [(3, 2), (3, 1)] # Cria um gargalo perigoso
        }
}