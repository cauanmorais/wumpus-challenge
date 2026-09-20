from gameLoop import GameLoop

def main():
    # --- Hyperparameters ---
    NUM_EPISODES = 1000
    MAX_STEPS = 30
    LEARNING_RATE = 0.05       
    
    # Exploration parameters
    exploration_rate = 1.0     
    min_exploration = 0.05     
    decay_rate = 0.99   

    # Epoch results
    win_counter = 0       

    print("Initializing Wumpus World AI...\n")
    game = GameLoop() 
    
    # --- Menu de Escolha do Mapa ---
    while True:
        print("Como você deseja configurar o mapa?")
        print("1 - Montar o mapa manualmente")
        print("2 - Gerar um mapa aleatório")
        escolha = input("Escolha a opção (1 ou 2): ").strip()

        if escolha == '1':
            print("\nIniciando configuração manual do mapa...")
            game.start()
            break
        elif escolha == '2':
            print("\nGerando mapa aleatório...")
            game.start_random()
            break
        else:
            print("\nErro: Opção inválida. Digite apenas 1 ou 2.\n")
            
    print("=" * 40)

    # --- The Training Loop ---
    for episode in range(1, NUM_EPISODES + 1):

        game.reset_game()
        game.game_map.display()

        # 2. Step Loop (The actual gameplay)
        for step in range(MAX_STEPS):
            # getAction automatically calls move_agent, which updates and prints the map for us!
            game.getAction(exploration=exploration_rate)
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
        if exploration_rate > min_exploration:
            exploration_rate *= decay_rate

        # 5. Progress Output 
        if episode == NUM_EPISODES:
            status = "WON!" if game.robot.found_gold else "Died/Timeout"
            print(f"Episode {episode}/{NUM_EPISODES} | Status: {status} | Score: {game.score} | Exploration: {exploration_rate:.2f}")
        else: 
            # Dica: Se 1000 prints de "Let's go" poluírem muito o terminal, 
            # você pode mudar para if episode % 50 == 0:
            print(f"Let's go for the epoch {episode + 1}")

    print("=" * 40)
    print("Training Complete! The Q-Table is now optimized for this maze.")
    print(f"The agent suceed {win_counter} times")
    print(f"killed monster {getattr(game, 'monsterKilledCounter', 0)} times")

if __name__ == "__main__":
    main()