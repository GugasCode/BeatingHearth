"""
Classifiers module that will have all of the classifiers being used in this
project, for now there is the kNN and the Naive Bayes classifiers.
"""
# Using Python 3
import numpy as np

class Bayes():
    """
            Class that will represent the Naive Bayes classifier.
    """
    def __init__(self, data):
        self.data = data
        self.data_size = len(data)
        pass

    def seperate(self):
        """
                Method that will seperate the existing data into the different
                classes of the data.
        """
        seperated = {}
        for item in data:
                key = itme[3]
                if key in data.keys():
                        seperated[key].append(item)
                else:
                        seperated[key] = [item]

        # new data already seperated between classes
        self.data = seperated

    def probabilities(self):
        """
                Method that will calculate all of the porbabilities of being from
                each class.
        """
        self.class_probs = {}
        for key, value in self.data:
                self.class_probs[key] = len(values)

    def conditionals(self, test, training_class, param):
        """
                Method to calculate the conditional probability for a specific
                parameter.
        """
        count = 0
        for element in self.data[training_class]:
            if element[param] == test[param]:
                count += 1
        count_x = 0
        for classes, values in self.data:
            for line in values:
                if line[param] == test[param]:
                    count_x += 1

        return (count/self.data[training_class])/(count_x/self.data_size)

    def bayes(self, test):
        """
            Method that will perform the entire algorithm from start to
            finish.
        """
        # seperate the data
        separated()

        # calculate the absolut probabilities (porbability of being of a class)
        probabilities()

        # get all of the probabilities to check which is highest
        results = {}
        for item in self.data.key():
            sums = 0
            for i in range(0,4):
                sums += log(conditional(test, item, i))
            results[item] = sums

        #finding the best fit after all of the calculations
        pivot = (0,0)
        for key, value in results.items():
            if value > pivot[1]:
                pivot = (key, value)

        #send the results
        return pivot[0]



class KNN():
    def __init__(self, data, k):
        self.data = data
        self.k = k

    def distance(self, test):
        size = len(test)-2
        dsitances = []
        for item in self.data:
                dist = 0
                for element in range(1, size):
                        dist += (item[element] - test[element])**2
                distances.append((item[0], dist))
        return distances

    def classify(self, test, k):
        distances = self.distance(test)
        distances.sort(key=operator.itemgetter(1))

        neighbors = []
        for x in range(k):
                neighbors.append(distances[x][0])
        return neighbors
