from gameLoop import GameLoop

def main():
    # --- Hyperparameters ---
    NUM_EPISODES = 1000        
    MAX_STEPS = 50             
    LEARNING_RATE = 0.05       
    
    # Exploration parameters
    exploration_rate = 1.0     
    min_exploration = 0.05     
    decay_rate = 0.99          

    print("Initializing Wumpus World AI...")
    # FIX 1: GameLoop requires maxLoops in its __init__
    game = GameLoop() 
    
    game.start()
    print("=" * 40)

    # --- The Training Loop ---
    for episode in range(1, NUM_EPISODES + 1):
        
        # 1. Reset the environment for the new episode
        
        # FIX 3: Capture the robot's LAST position before we reset it
        old_pos = game.robot.position()
        
        game.robot.reset()
        game.robot.record.clear()
        game.score = 0.0
        game.glitter = False
        
        new_pos = game.robot.position() # This will be (1, 1) after reset
        
        # FIX 2 & 3: Use update_ui to visually erase the old 'R' and draw it at (1, 1)
        # We wrap this in an 'if' so we don't accidentally erase the starting line on Episode 1
        if old_pos != new_pos:
            game.update_ui(oldPosition=old_pos, oldValue='.', newPosition=new_pos, newValue='R')

        # 2. Step Loop (The actual gameplay)
        for step in range(MAX_STEPS):
            
            # getAction automatically calls move_agent, which updates and prints the map for us!
            game.getAction(exploration=exploration_rate)

            # Check if the episode should end immediately
            if not game.robot.alive:
                break 
            if game.glitter:
                break 

        # 3. Post-Episode Learning
        game.updatePolicy(learningRate=LEARNING_RATE)

        # 4. Decay Exploration
        if exploration_rate > min_exploration:
            exploration_rate *= decay_rate

        # 5. Progress Output 
        if episode % 50 == 0:
            status = "WON!" if game.glitter else "Died/Timeout"
            print(f"Episode {episode}/{NUM_EPISODES} | Status: {status} | Score: {game.score} | Exploration: {exploration_rate:.2f}")

    print("=" * 40)
    print("Training Complete! The Q-Table is now optimized for this maze.")
    print("Starting position probabilities:", game.Q[1][1])

if __name__ == "__main__":
    main()