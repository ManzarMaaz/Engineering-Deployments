from Environment import *
import math

class Agent:
    def __init__(self, ob: Environment):
        self.total_rewards = 0
        self.penalty = 0
        self.ob = ob

    def predictCondition(self, X_train, y_train, testData):
        predict = self.ob.action(X_train, y_train, testData)
        return predict

    # agent step function always monitor environemnt and call action to
    # field condition
    def step(self, X_train, y_train, X_test, y_test):
        self.total_rewards = 0
        self.penalty = 0
        for i in range(len(X_test)):
            predict = self.ob.action(X_train, y_train, X_test[i])
            if predict == y_test[i]:
                self.total_rewards += 1
            else:
                self.penalty += 15
        return self.total_rewards, self.penalty