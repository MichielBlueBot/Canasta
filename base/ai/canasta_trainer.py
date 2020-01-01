import datetime
from collections import defaultdict

import numpy as np
import tensorflow as tf

from base.action_service import ActionService
from base.ai.canasta_env import CanastaEnv


class MyModel(tf.keras.Model):
    def __init__(self, num_states, num_hidden_units, num_actions):
        super(MyModel, self).__init__()
        self.input_layer = tf.keras.layers.InputLayer(input_shape=(num_states,))
        self.hidden_layers = []
        for i in num_hidden_units:
            self.hidden_layers.append(tf.keras.layers.Dense(i, activation='tanh', kernel_initializer='RandomNormal'))
        self.output_layer = tf.keras.layers.Dense(
            num_actions, activation='linear', kernel_initializer='RandomNormal')

    @tf.function
    def call(self, inputs, mask):
        z = self.input_layer(inputs)
        for layer in self.hidden_layers:
            z = layer(z)
        output = self.output_layer(z)
        output *= tf.cast(mask, tf.float32)   # apply mask
        # output /= tf.norm(output, axis=1)   # renormalize
        return output


class DQN:
    def __init__(self, num_states, num_actions, hidden_units, gamma, max_experiences, min_experiences, batch_size, lr):
        self.num_actions = num_actions
        self.batch_size = batch_size
        self.optimizer = tf.optimizers.Adam(lr)
        self.gamma = gamma
        self.model = MyModel(num_states, hidden_units, num_actions)
        self.experience = defaultdict(list)
        self.max_experiences = max_experiences
        self.min_experiences = min_experiences

    def predict(self, inputs, masks):
        return self.model(np.atleast_2d(inputs.astype('float32'), masks.astype('float32')))

    @tf.function
    def train(self, target_net):
        if len(self.experience['s']) < self.min_experiences:
            return 0
        ids = np.random.randint(low=0, high=len(self.experience['s']), size=self.batch_size)
        states = np.asarray([self.experience['s'][i] for i in ids])
        masks = np.asarray([self.experience['m'][i] for i in ids])
        actions = np.asarray([self.experience['a'][i] for i in ids])
        rewards = np.asarray([self.experience['r'][i] for i in ids])
        states_next = np.asarray([self.experience['s2'][i] for i in ids])
        dones = np.asarray([self.experience['done'][i] for i in ids])
        value_next = np.max(target_net.predict(states_next), axis=1)
        actual_values = np.where(dones, rewards, rewards+self.gamma*value_next)

        with tf.GradientTape() as tape:
            selected_action_values = tf.math.reduce_sum(
                self.predict(states, masks) * tf.one_hot(actions, self.num_actions), axis=1)
            loss = tf.math.reduce_sum(tf.square(actual_values - selected_action_values))
        variables = self.model.trainable_variables
        gradients = tape.gradient(loss, variables)
        self.optimizer.apply_gradients(zip(gradients, variables))

    def get_action(self, states, mask, epsilon):
        if np.random.random() < epsilon:
            valid_actions_indexes = [idx for idx, is_valid in enumerate(mask) if is_valid]
            return np.random.choice(valid_actions_indexes)
        else:
            return np.argmax(self.predict(np.atleast_2d(states), np.atleast_2d(mask))[0])

    def add_experience(self, exp):
        if len(self.experience['s']) >= self.max_experiences:
            for key in self.experience.keys():
                self.experience[key].pop(0)
        for key, value in exp.items():
            self.experience[key].append(value)

    def copy_weights(self, train_net):
        variables1 = self.model.trainable_variables
        variables2 = train_net.model.trainable_variables
        for v1, v2 in zip(variables1, variables2):
            v1.assign(v2.numpy())


def play_game(env, train_net, target_net, epsilon, copy_step, print_exp_step):
    rewards = 0
    iteration = 0
    done = False
    observations = env.reset()
    while not done:
        actions_mask = env.get_current_actions_mask()
        action = train_net.get_action(observations, actions_mask, epsilon)
        prev_observations = observations
        observations, reward, done, _ = env.step(action)
        rewards += reward
        if done:
            reward = -200
            env.reset()

        exp = {'s': prev_observations, 'a': action, 'r': reward, 'm': actions_mask, 's2': observations, 'done': done}
        train_net.add_experience(exp)
        train_net.train(target_net)
        iteration += 1
        if iteration % print_exp_step == 0:
            print("Experience replay:")
            for exp_action in train_net.experience['a']:
                print(ActionService().idx_to_action(exp_action))
        if iteration % copy_step == 0:
            target_net.copy_weights(train_net)
    return rewards


def main():
    env = CanastaEnv()
    gamma = 0.99
    copy_step = 25
    print_exp_step = 10
    num_states = env.observation_space.n
    num_actions = env.action_space.n
    hidden_units = [200, 200]
    max_experiences = 10000
    min_experiences = 100
    batch_size = 32
    lr = 1e-2
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = 'logs/dqn/' + current_time
    summary_writer = tf.summary.create_file_writer(log_dir)

    train_net = DQN(num_states, num_actions, hidden_units, gamma, max_experiences, min_experiences, batch_size, lr)
    target_net = DQN(num_states, num_actions, hidden_units, gamma, max_experiences, min_experiences, batch_size, lr)
    number_iterations = 50
    total_rewards = np.empty(number_iterations)
    epsilon = 0.99
    decay = 0.9999
    min_epsilon = 0.1
    avg_rewards = 0
    for n in range(number_iterations):
        epsilon = max(min_epsilon, epsilon * decay)
        total_reward = play_game(env, train_net, target_net, epsilon, copy_step, print_exp_step)
        total_rewards[n] = total_reward
        avg_rewards = total_rewards[max(0, n - 100):(n + 1)].mean()
        with summary_writer.as_default():
            tf.summary.scalar('episode reward', total_reward, step=n)
            tf.summary.scalar('running avg reward(100)', avg_rewards, step=n)
        if n % 100 == 0:
            print("episode:", n, "episode reward:", total_reward, "eps:", epsilon, "avg reward (last 100):", avg_rewards)
    print("avg reward for last 100 episodes:", avg_rewards)
    env.close()


if __name__ == '__main__':
    main()
