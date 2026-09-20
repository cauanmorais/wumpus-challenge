from gameLoop import GameLoop
from test_maps import MAPAS_TESTE
from constants import (
    DEBUG_MODE, NUM_EPISODES, MAX_STEPS, LEARNING_RATE, 
    INITIAL_EXPLORATION_RATE, MIN_EXPLORATION, DECAY_RATE
)

def main():
    # Epoch results
    win_counter = 0       

    exploration_rate = INITIAL_EXPLORATION_RATE

    print("Initializing Wumpus World AI...\n")
    game = GameLoop() 
    
    while True:
        print("Como você deseja configurar o mapa?")
        print("1 - Montar o mapa manualmente")
        print("2 - Gerar um mapa aleatório")
        print("3 - Escolher um mapa de testes pré-definido")
        escolha = input("Escolha a opção (1, 2 ou 3): ").strip()

        if escolha == '1':
            print("\nIniciando configuração manual do mapa...")
            game.start()
            break
            
        elif escolha == '2':
            print("\nGerando mapa aleatório...")
            game.start_random()
            break
            
        elif escolha == '3':
            # --- Submenu de Mapas de Teste ---
            print("\nMapas de Teste Disponíveis:")
            for chave, mapa in MAPAS_TESTE.items():
                print(f"{chave} - {mapa['nome']}")
                
            escolha_teste = input("Qual mapa você quer testar? ").strip()
            
            if escolha_teste in MAPAS_TESTE:
                print(f"\nCarregando: {MAPAS_TESTE[escolha_teste]['nome']}...")
                game.start_test_map(MAPAS_TESTE[escolha_teste])
                break
            else:
                print("Opção inválida. Retornando ao menu principal...\n")
                
        else:
            print("\nErro: Opção inválida. Digite 1, 2 ou 3.\n")
            
    print("=" * 40)

    # --- The Training Loop ---
    for episode in range(1, NUM_EPISODES + 1):

        game.reset_game()
        if DEBUG_MODE:
            game.game_map.display()

        # 2. Step Loop (The actual gameplay)
        for step in range(MAX_STEPS):
            game.getAction(exploration=exploration_rate)
            if DEBUG_MODE:
                game.game_map.display()
                game.showCurrentState()
            
            # Check if the episode should end immediately
            if not game.robot.alive:
                break 
            if game.robot.found_gold:
                win_counter += 1
                break

        # 3. Post-Episode Learning
        game.updatePolicy(learningRate=LEARNING_RATE)

        # 4. Decay Exploration
        if exploration_rate > MIN_EXPLORATION:
            exploration_rate *= DECAY_RATE

        # 5. Progress Output 
        if episode == NUM_EPISODES:
            status = "WON!" if game.robot.found_gold else "Died/Timeout"
            print(f"Episode {episode}/{NUM_EPISODES} | Status: {status}")
        else: 
            if DEBUG_MODE:
                print(f"Let's go for the epoch {episode + 1}")

    print("=" * 40)
    print("Training Complete! The Q-Table is now optimized for this maze.")
    print(f"The agent suceed {win_counter} times")
    print(f"killed monster {getattr(game, 'monsterKilledCounter', 0)} times")
    print(f"The success rate was: {((win_counter / NUM_EPISODES) * 100):.2f}%")

if __name__ == "__main__":
    main()