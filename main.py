from gameLoop import GameLoop

def main():
    # --- Hyperparameters ---
    NUM_EPISODES = 1000
    MAX_STEPS = 15
    LEARNING_RATE = 0.05       
    win_counter = 0
    
    # Exploration parameters
    exploration_rate = 1.0     
    min_exploration = 0.05     
    decay_rate = 0.99          

    print("Initializing Wumpus World AI...")
    print()
    game = GameLoop() 
    
    game.start()

    print("Starting position probabilities:", game.Q[1][1])
    # --- The Training Loop ---
    for episode in range(1, NUM_EPISODES + 1):

        # 1. Reset the environment for the new episode
        old_pos = game.robot.position()
        robot_found_gold = game.robot.found_gold

        game.robot.reset()
        game.score = 0.0
        
        new_pos = game.robot.position() # This will be (1, 1) after reset
        
        if old_pos != new_pos and not robot_found_gold:
            game.update_ui(oldPosition=old_pos, oldValue='.', newPosition=new_pos, newValue='R')
            game.game_map.display()
        #If the robot found the gold, the last position is G not .
        elif old_pos != new_pos and robot_found_gold:
                    game.update_ui(oldPosition=old_pos, oldValue='G', newPosition=new_pos, newValue='R')
                    game.game_map.display()

        # 2. Step Loop (The actual gameplay)
        for step in range(MAX_STEPS):
            # getAction automatically calls move_agent, which updates and prints the map for us!
            game.getAction(exploration=exploration_rate)
            

            # Check if the episode should end immediately
            if not game.robot.alive:
                break 
            if game.robot.found_gold:
                win_counter += 1
                gold_location = game.robot.position()
                break

        # 3. Post-Episode Learning
        game.updatePolicy(learningRate=LEARNING_RATE)

        # 4. Decay Exploration
        if exploration_rate > min_exploration:
            exploration_rate *= decay_rate

        print(f"Let's go for the epoch {episode + 1}")

        # 5. Progress Output 
        if episode % 50 == 0:
            status = "WON!" if game.robot.found_gold else "Died/Timeout"
            print(f"Episode {episode}/{NUM_EPISODES} | Status: {status} | Score: {game.score} | Exploration: {exploration_rate:.2f}")

    print("=" * 40)
    print("Training Complete! The Q-Table is now optimized for this maze.")
    print("Starting position probabilities:", game.Q[1][1])
    print(f"The agent suceed {win_counter} times")

if __name__ == "__main__":
    main()