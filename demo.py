from game import SnakeGame
from agent import Agent
from utils import *

import torch as T
import numpy as np
import glob, os
from datetime import datetime

plot_name = 'demo.png'
video_name = 'demo.mp4'
target_folder = "demo"
n_episodes = 20
pretrained_weights = "weights/latest.pt"

if __name__ == '__main__':

    #delete all frames from the previous demo
    print("removing all frames from previous demo")
    for i in glob.glob(f"{target_folder}/*jpg"):
        os.remove(i)
    print("removed")

    env = SnakeGame()
    agent = Agent(gamma = 0.99, epsilon = 0.0,  batch_size = 64, n_actions = 4,eps_end = 0.01, input_dims = [12], lr = 0.0)
    
    print(f"loading pretrained weights from {pretrained_weights}...")
    agent.Q_eval.load_state_dict(T.load(pretrained_weights))
    agent.Q_eval.eval()
    # new=list(pre_trained_model.items())
    # my_model_kvpair=agent.Q_eval.state_dict()
    # count=0
    # for key,value in my_model_kvpair.item():   
    #     layer_name,weights=new[count]      
    # mymodel_kvpair[key]=weights
    # count+=1
    print("weights loaded.")

    scores, eps_history, avg_scores, frames = [] , [] , [] ,[] #frames will not be in use
    n_games = n_episodes

    for i in range(n_games):
        score = 0
        step = 0
        done = False
        observation = env.reset()
        # frames.append(env.animate(i,step,score))
        snake_len = len(env.snake)
        frame = env.animate(i,step,score,snake_len)
        frame.save(f"{target_folder}/ep{i}step{step}.jpg","jpeg")

        while not done:
            step += 1
            action = agent.choose_action(observation)
            observation_, reward, done = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            # agent.learn() #don't learn since this is a demo
            observation = observation_
            snake_len = len(env.snake)
            frame = env.animate(i,step,score,snake_len)
            frame.save(f"{target_folder}/ep{i}step{step}.jpg","jpeg")
            # frames.append(frame)
        scores.append(score)
        
        eps_history.append(agent.epsilon)
        avg_score = np.mean(scores[-100:]) #mean of last 100 scores
        avg_scores.append(avg_score)

        print('episode ', i , 'score %.2f' % score, 'average score %.2f' % avg_score, 'epsilon %.2f' % agent.epsilon, 'length: ',snake_len)
    

    now = datetime.now()
    # current_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    # T.save(agent.Q_eval.state_dict(), f"weights/{current_time}.pt")
    x = [i + 1 for i in range(n_games)]
    plot_results(x,scores,avg_scores,eps_history,plot_name)
    save_mp4(target_folder,video_name)


