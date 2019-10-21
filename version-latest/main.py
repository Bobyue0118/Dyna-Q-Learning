from agent import Agent, Model #import class Agent from agent
import time

maze = '2'

if maze == '1':
    from maze_env1 import Maze
elif maze == '2':
    from maze_env2 import Maze


if __name__ == "__main__":
    ### START CODE HERE ###
    # This is an agent with random policy. You can learn how to interact with the environment through the code below.
    # Then you can delete it and write your own code.

    episodes             = 100
    model_based_episodes = 5
    env   = Maze()
    model = Model(actions=list(range(env.n_actions)))
    agent = Agent(actions=list(range(env.n_actions)))       # 从range(4)，也就是0,1,2,3（上下右左）四个行为中选择
    for episode in range(episodes):                         # 对于每一段，从开始到结束
        s = env.reset()
        episode_reward = 0
        while True:
            #env.render()                 # You can comment all render() to turn off the graphical interface in training process to accelerate your code.

            # move one step
            a = agent.choose_action(str(s))

            s_, r, done = env.step(a)

            # update Q model-free
            agent.update(str(s), a, r, str(s_), done)

            model.store_transition(str(s), a, r, s_)

            # update Q model-based
            for n in range(model_based_episodes):
                ss, sa  = model.sample_s_a()
                sr, ss_ = model.get_r_s_(ss, sa)
                agent.update(ss, sa, sr, str(ss_), done)

            episode_reward += r
            s = s_

            if done:
                #env.render()
                time.sleep(0.5)
                break

        # format output
        print('episode: %2s'%episode, 'episode_reward: %2s'%episode_reward)

    ### END CODE HERE ###

    print('\ntraining over\n')