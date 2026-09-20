# 🏹 Wumpus World AI - Q-Learning

Este projeto é uma implementação em Python do clássico **Mundo de Wumpus (Wumpus World)**, resolvida por um agente autônomo movido a Inteligência Artificial. O agente utiliza **Aprendizado por Reforço (Reinforcement Learning)** para explorar o mapa, desviar de armadilhas, matar o monstro e encontrar o ouro.

---

## 🧠 Como a IA funciona (O Algoritmo)

O "cérebro" do robô é alimentado pelo algoritmo de **Q-Learning**, uma técnica de aprendizado por tentativa e erro:

1. **A Tabela Q (Q-Table):** O agente possui uma matriz 3D onde mapeia cada coordenada `(X, Y)` e as possíveis ações (Cima, Baixo, Esquerda, Direita, Atirar). Ele começa sem saber nada (todos os valores são iguais).
2. **Recompensas e Punições:** 
   - Cair num poço ou ser comido pelo Wumpus: **-1000 pontos** (Punição severa).
   - Bater na parede: **-10 pontos**.
   - Encontrar o ouro: **+1000 pontos** (Recompensa máxima).
   - Andar (custo de energia): **-1 ponto**.
3. **Exploração vs. Explotação (Epsilon-Greedy):** Nas primeiras rodadas, o robô toma decisões 100% aleatórias para explorar o mapa. A cada tentativa (episódio), essa aleatoriedade cai (Decay Rate). No final, ele confia apenas na experiência adquirida (probabilidades da Q-Table) para fazer a rota perfeita.

---

## 🗺️ A Lógica do Jogo

O mapa é um grid fechado contendo:
* **(G) Ouro:** O objetivo principal.
* **(P) Poços:** Morte instantânea. O robô sente uma **Brisa** nas casas adjacentes.
* **(W) Wumpus:** O monstro. Morte instantânea. O robô sente um **Fedor** nas casas adjacentes. Pode ser morto se o robô atirar uma flecha na sua direção.
* **(R) Robô:** O agente que deve navegar pelo mapa.

> **Nota:** A geração aleatória do mapa utiliza um algoritmo de **Busca em Largura (BFS)** para garantir que o ouro sempre seja alcançável, evitando cenários impossíveis.

---

## ⚙️ Configurando a IA (Hiperparâmetros)

Todo o comportamento de aprendizado do robô pode ser calibrado editando o arquivo `constants.py`. Isso permite que você teste como a IA reage a diferentes ritmos de aprendizado.

| Parâmetro | Descrição |
| :--- | :--- |
| `DEBUG_MODE` | Defina como `True` para ver o mapa sendo desenhado passo a passo no terminal. Defina como `False` para realizar o treinamento silencioso de forma ultra-rápida (recomendado para mais de 1.000 episódios). |
| `NUM_EPISODES` | Quantas "vidas" o robô terá para tentar resolver o mapa. Quanto maior, mais inteligente ele fica (ex: `100000`). |
| `MAX_STEPS` | Limite de movimentos por episódio. Evita que a IA fique andando em círculos infinitamente. (ex: `30`). |
| `LEARNING_RATE` | (Alpha) Define o quão rápido a IA substitui seu conhecimento antigo por novas informações. Valores altos (ex: `0.1`) fazem ela aprender rápido, mas de forma instável. Valores baixos (ex: `0.05`) geram um aprendizado mais lento e consolidado. |
| `INITIAL_EXPLORATION_RATE` | Taxa inicial de ações aleatórias. `1.0` significa que no episódio 1, 100% dos movimentos serão aleatórios (exploração pura). |
| `MIN_EXPLORATION` | O limite mínimo de aleatoriedade. Mesmo super inteligente, o robô mantém uma pequena chance (ex: `0.05` ou 5%) de tentar algo novo. |
| `DECAY_RATE` | O fator de redução da exploração. A cada episódio, a aleatoriedade é multiplicada por esse valor (ex: `0.99`), forçando o robô a parar de "chutar" e começar a usar o que aprendeu. |

---

## 📂 Estrutura do Projeto

* `main.py`: O ponto de entrada. Gerencia o menu interativo e o loop de treinamento (Episódios).
* `gameLoop.py`: O maestro do jogo. Atualiza a pontuação, move o agente e aplica a matemática do Q-Learning.
* `gameMap.py`: Gerencia o grid, posições, sensores e o algoritmo BFS para geração e validação de mapas.
* `entities/robot.py`: Classe que define o estado do robô, seu histórico de movimentos e as ações de andar/atirar.
* `constants.py`: Dicionário global de constantes matemáticas para movimentação (Clean Code).
* `test_maps.py`: Um banco de dados com mapas estáticos pré-configurados (Fácil, Médio, Difícil) para testar a eficiência do agente.

---

## 🚀 Como Usar

### Pré-requisitos
* Python 3.x instalado.
* Biblioteca **NumPy** (Usada para otimização matemática avançada na Q-Table).

Para instalar as dependências:
```bash
pip install numpy
```

### Rodando o Projeto

Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

Um menu interativo será exibido oferecendo 3 opções:

1. **Montar o mapa manualmente:** Você digita as coordenadas (X, Y) do Ouro, Poços e Wumpus.
2. **Gerar um mapa aleatório:** O sistema cria um mapa dinâmico resolvível.
3. **Escolher um mapa de testes:** Selecione mapas pré-definidos (como "Corredor da Morte") para ver como a IA reage a desafios específicos.

Acompanhe o terminal enquanto o robô morre, aprende e, finalmente, domina o mapa!
