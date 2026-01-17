from numpy import dot
from numpy.linalg import norm

class Environment:
    # Agent will call environment action function to predict field condition
    def action(self, train_data, train_label, test_data):
        label = None
        score = 0
        for i in range(0, 100):
            # Calculate cosine similarity
            predict = dot(train_data[i], test_data) / (norm(train_data[i]) * norm(test_data))
            if predict > score:
                score = predict
                label = train_label[i]
        return label