import numpy as np

from copy import copy

START_TOKEN = "START_TOKEN"
END_TOKEN = "END_TOKEN"


class MarkovChain:
    def __init__(self, states=None):
        if not states:
            states = []

        self.states = states
        self.T = np.zeros((len(self.states), len(self.states)))

    def add_state(self, state):
        self.states.append(state)
        b, self.T = copy(self.T), np.zeros((self.T.shape[0] + 1, self.T.shape[0] + 1))
        self.T[:-1, :-1] = b

    def add_states(self, states):
        for state in states:
            self.add_state(state)

    def get_state_index(self, state):
        if state not in self.states:
            return None
        return self.states.index(state)

    def train_with_sentences(self, sentences):
        for sentence in sentences:
            sentence = sentence.strip("b").strip("'").strip('"').split(" ")

            for i in range(len(sentence)):
                word = sentence[i]
                if word == END_TOKEN:
                    break
                if word not in self.states:
                    continue

                next_word = sentence[i+1]
                if next_word not in self.states:
                    continue

                origin_idx = self.get_state_index(word)
                dest_idx = self.get_state_index(next_word)
                self.T[origin_idx][dest_idx] += 1.0

        self.to_probability()

    def to_probability(self):
        n_rows, n_columns = self.T.shape

        for i in range(n_rows):
            total_row = sum(self.T[i])
            if total_row == 0.0:
                continue

            for j in range(n_columns):
                self.T[i][j] = self.T[i][j] / total_row
