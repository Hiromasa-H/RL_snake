from game import SnakeGame
from agent import Agent
from utils import *

import torch as T
import numpy as np
import glob, os
import sys
from datetime import datetime

# plot_name = 'result.png'
# video_name = 'result.mp4'
# target_folder = "frames"
# n_episodes = 10000

plot_name = 'debug.png'
video_name = 'debug.mp4'
target_folder = "debug"
n_episodes = 10

if __name__ == '__main__':

    #delete all frames from the previous training
    print("removing all frames from previous training")
    n_files = len([name for name in os.listdir(target_folder)])
    cntr = 0
    for i in glob.glob(f"{target_folder}/*jpg"):
        sys.stdout.write('\r')
        sp = cntr/((n_files-1)/100)
        tp = int(sp/4)
        sys.stdout.write("[%-25s] %d%%" % ('='*tp, sp)) #25s=25spaces
        sys.stdout.flush()
        os.remove(i)
        cntr += 1
    print("removed")

    env = SnakeGame()
    agent = Agent(gamma = 0.99, epsilon = 1.0,  batch_size = 64, n_actions = 4,eps_end = 0.01, input_dims = [16], lr = 0.003)
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
            agent.learn()
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
    current_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    T.save(agent.Q_eval.state_dict(), f"weights/{current_time}.pt")
    x = [i + 1 for i in range(n_games)]
    plot_results(x,scores,avg_scores,eps_history,plot_name)
    save_mp4(target_folder,video_name)


