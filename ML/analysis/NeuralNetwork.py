# -*- coding: utf-8 -*-
import numpy as np
import json
import os.path

class NeuralNetwork:

    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    NUM_INPUT: The number of input units (without bias term)
    NUM_HIDDEN: The number of hidden units (without bias term)
    NUM_OUTPUT: The number of output units 
    Func_h1: activate function in hidden layer
    Func_h2: activate function in output layer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    def __init__(self, user_id, NUM_INPUT, NUM_HIDDEN, NUM_OUTPUT, learning_rate):
        # user_id : '''STRING''' shape
        self.user_id = user_id
        #param
        self.NUM_INPUT = NUM_INPUT +1
        self.NUM_HIDDEN = NUM_HIDDEN +1
        self.NUM_OUTPUT = NUM_OUTPUT

        result = self.is_fileExist(self.user_id)
        if result == False:
            # if the user_id is the new id, then generate weights randomly
            weights = self.generateWeightsFile(self.user_id)
        else:
            # if the file exists, retrieve the weight 
            weights = self.pullDownfromFile(self.user_id)
        self.w1, self.w2 = self.setWeights(weights)
        
        # init vec values of each layer, set to 0
        self.z1 = np.zeros(self.NUM_INPUT) # same as x, which is input vec
        self.z2 = np.zeros(self.NUM_HIDDEN)
        self.z3 = np.zeros(self.NUM_OUTPUT)
        self.u2 = np.zeros(self.NUM_HIDDEN)
        self.u3 = np.zeros(self.NUM_OUTPUT)
        # set the bias term
        self.z1[0] = 1
        self.z2[0] = 1

        #init the delta
        self.d2 = np.zeros(self.NUM_HIDDEN)
        self.d3 = np.zeros(self.NUM_OUTPUT)

        self.learning_rate = learning_rate


    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ### Activate functions & differential calculus ###
    1. sigmoid function
    2. tanh function
    3. softmax function
    4. differential calculus of tanh
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    def sigmoid_func(self, u):
        if u < -700:
            return 0.00
        else:
            return 1/(1+np.exp(-u))

    def tanh_func(self, u):
        u /= 1000
        return (np.exp(u) - np.exp(-u))/(np.exp(u) + np.exp(-u))

    def softmax_func(self, u):
        return np.exp(u) / sum(np.exp(u))

    def diff_tanh(self, u):
        return - 2 * np.exp(-u) / (np.exp(u) + np.exp(-u))**2



    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ### Neural Network ~ main part ~ ###
    1. feedForward process
        This is used both in learning process and output process for recommendataion
    2. backPropagation process 
        this part is used only in learning process (updating weights)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    

    def feedForward(self, x, weights='main'):
        if len(x) != len(self.z1)-1:
            print 'Something wrong with input size!'
            return 

        # Bias term x[0] = 1 
        self.z1 = np.array(x)
        self.z1 = np.insert(x, 0, 1)

        if weights != 'main':
            # set the weights
            self.w1 = weights['w1']
            self.w2 = weights['w2']

        ## feedForwardProcess 
        ### first step: calc output of hidden layer ###
        #u2 = np.zeros(self.NUM_HIDDEN)
        #for j in range(self.NUM_HIDDEN):
            #u2[j] = np.dot(np.transpose(self.w1)[j], self.z1)
            #this u2[j] value is too big such as 4000
        self.u2 = np.array([np.dot(np.transpose(self.w1)[j], self.z1) for j in range(self.NUM_HIDDEN)])
        # using tanh function
        self.z2 = self.tanh_func(self.u2)

        ### second step: calc output of output layer ###
        #u3 = np.zeros(self.NUM_OUTPUT)
        #for k in range(self.NUM_OUTPUT):
            #u3[k] = np.dot(np.transpose(self.w2)[k], self.z2)
        self.u3 = np.array([np.dot(np.transpose(self.w2)[k], self.z2) for k in range(self.NUM_OUTPUT)])
        # using softmax function
        self.z3 = self.softmax_func(self.u3)
                    
        # return the output
        return self.z3
    


    def backPropagation(self, category, feedback):

        t = np.zeros(self.NUM_OUTPUT)
        t[category-1] = feedback
        self.d3 = t - self.z3

        # back propagation
        diff_tanh_u2 = self.diff_tanh(self.u2)
        for j in range(self.NUM_HIDDEN):
            self.d2[j] = np.dot(self.d3, self.w2[j]) * diff_tanh_u2[j]
        
        d_En1 = np.random.random((self.NUM_INPUT, self.NUM_HIDDEN))
        d_En2= np.random.random((self.NUM_HIDDEN, self.NUM_OUTPUT))


        #value of delta in hidden layer : d2
        ## dEn/dW1_ji = d2_j * z1_i
        d_En1 = [[self.d2[j] * self.z1[i] for j in range(self.NUM_HIDDEN)] for i in range(self.NUM_INPUT)]

        #value of delta in output layer : d3
        ## dEn/dW2_ji = d3_j * z2_i
        d_En2 = [[self.d3[j] * self.z2[i] for j in range(self.NUM_OUTPUT)] for i in range(self.NUM_HIDDEN)]

        #fixing weights: dW_(n+1) = dW_(n) - learning_rate * d_En
        #self.w1 = self.w1 - self.learning_rate * d_En1
        #self.w2 = self.w2 - self.learning_rate * d_En2
        self.w1 = [[self.w1[i][j]-d_En1[i][j]*self.learning_rate for j in range(self.NUM_HIDDEN)] for i in range(self.NUM_INPUT)]
        self.w2 = [[self.w2[i][j]-d_En2[i][j]*self.learning_rate for j in range(self.NUM_OUTPUT)] for i in range(self.NUM_HIDDEN)]

        weights = {'w1': self.w1, 'w2': self.w2}
        return weights




    def startLearning(self, actions_data):
        """
        actions_data = [action_data_1, action_data_2, ...., action_data_N]
        ex. action_data_i = ["day", "time", "temperature", "weather", "freqency", "feedback", "user_id", "song_id", "category_id"]
        ==> normalized vector (all elems are float & int)
        """
        weights = {'w1': self.w1, 'w2': self.w2}
        for action in actions_data:
            input_data = action[:6]
            category = action[8]
            feedback = action[5]
            self.feedForward(input_data, weights)
            new_weights = self.backPropagation(category, feedback)
            weights = new_weights

        return weights



   
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ### weights management ###
    1. setWeights:
        This is used when weights are pulled down from json 
        to format data for neuralnetwork

    2. setWeights_JsonFormat: 
        This is used when weights are saved to json file
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    def setWeights(self, weights):
        weight1 = weights['w1']
        weight2 = weights['w2']
        w1 = []
        w2 = []
        # set w1
        for i in range(len(weight1)):
            w_x = 'w_' + str(i)
            w1.append(weight1[w_x])
            
        # set w2
        for i in range(len(weight2)):
            w_x = 'w_' + str(i)
            w2.append(weight2[w_x])
         
        #w1 = np.random.random((self.NUM_INPUT, self.NUM_HIDDEN))
        #w2 = np.random.random((self.NUM_HIDDEN, self.NUM_OUTPUT))
        return w1, w2

        """
        w = list(w)
        w_1 = w[0:self.NUM_INPUT*self.NUM_HIDDEN]
        w_2 = w[self.NUM_INPUT*self.NUM_HIDDEN:]
        self.w1 = np.array(w_1).reshape(NUM_INPUT, NUM_HIDDEN)
        self.w2 = np.array(w_2).reshape(NUM_HIDDEN, NUM_OUTPUT)
        """


    def setWeights_JsonFormat(self, weights):
        """
        Input layer (I): number of params
        hidden layer (H): setting apropriately
        output layer (O): number of categories
        [I, H, O] = [6, 5, 10] --include bias terms -->> [7, 6, 10]

        ##json formated weights should be like this.
        weights = {
                    w1:{
                        w_0: [w_00, w_01, ..., w_05],
                        w_1: [w_10, w_11, ..., w_15],
                        ...                      ..., 
                        w_6: [w_60, w_61, ..., w_65]
                        }, 
                    w2:{
                        w_0: [w_00, w_01, ..., w_09],
                        w_1: [w_10, w_11, ..., w_19],
                        ...                      ..., 
                        w_5: [w_50, w_51, ..., w_59]
                        },
                    }
        """

        weights_json = {}
        w1 = {}
        w2 = {}
        weight1 = weights['w1']
        weight2 = weights['w2']

        #set w1
        for i in range(self.NUM_INPUT):
            w_x = 'w_'+ str(i)
            w_row = []
            [w_row.append(weight1[i][j]) for j in range(self.NUM_HIDDEN)]
            w1[w_x] = w_row

        #set w2
        for i in range(self.NUM_HIDDEN):
            w_x = 'w_'+ str(i)
            w_row = []
            [w_row.append(weight2[i][j]) for j in range(self.NUM_OUTPUT)]
            w2[w_x] = w_row

        weights_json['w1'] = w1
        weights_json['w2'] = w2
        return weights_json



    def generateRandomWeights(self):
        #init randomly
        weight1 = np.random.random((self.NUM_INPUT, self.NUM_HIDDEN))
        weight2 = np.random.random((self.NUM_HIDDEN, self.NUM_OUTPUT))
        weights = {'w1': weight1, 'w2': weight2}
        weights_json = self.setWeights_JsonFormat(weights)
        return weights_json

    


    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ### File management ###

    1. is_fileExist:
        This is for checking the existing file 

    2. generateWeightsFile:
        Generate new user's weights file to path: ./weights as "user_id".json
        weights are selected rondomly

    3. pullUptoFile: 
        new weights will be saved to ./weights/"user_id".json 

    4. pullDownfromFile: 
        previous weights will be pulling down fromm ./weights/"user_id".json
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    def is_fileExist(self, user_id):
        dir = os.path.dirname(__file__)
        relative_path = './weights/'+user_id+'.json'
        filename = os.path.join(dir, relative_path)
        result = os.path.isfile(filename)
        return result


    def generateWeightsFile(self, user_id):
        dir = os.path.dirname(__file__)
        relative_path = './weights/'+user_id+'.json'
        filename = os.path.join(dir, relative_path)

        weights = self.generateRandomWeights()
        with open(filename, 'w') as file:
            json.dump(weights, file, sort_keys=True, indent=4)



    def pullUptoFile(self, user_id, data):
        dir = os.path.dirname(__file__)
        relative_path = './weights/'+user_id+'.json'
        filename = os.path.join(dir, relative_path)

        with open(filename, 'w') as file:
            json.dump(data, file, sort_keys=True, indent=4)


    def pullDownfromFile(self, user_id):
        dir = os.path.dirname(__file__)
        relative_path = './weights/'+user_id+'.json'
        filename = os.path.join(dir, relative_path)

        with open(filename, 'r') as file:
            weights = json.load(file) 
        return weights





def getUserActions(user_id):
    """ 
    pull down user's actions(histories) from mongo db
    """
    actions_data = []
    user_id = int(user_id)

    from Recommendation import preProcessData
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    # connect to db 'prefy'
    db = client.prefy
    #get collection
    user_songs = db.songs
    user_actions = db.histories
    user_feedbacks = db.feedbacks

    #action_data_i = ["day", "time", "temperature", "weather", "freqency", "feedback", "user_id", "song_id", "category_id"]
    for user_song in user_songs.find({"user": user_id}):
        song_id = user_song['_id']
        song_genre = user_song['genre']
        song_freq = user_song['playtimes']

        actions = []
        for user_action in user_actions.find({"song": song_id}):
            action_date = user_action['date'] 
            action_weather = user_action['weather']
            #action_weather = np.random.random()
            action_time = user_action['time']
            #action_temp = (np.random.random()+0.5)*20
            action_temp = user_action['temp']
            action = [action_date, action_time, action_temp, action_weather]
            actions.append(action)

        feedbacks = []
        for user_feedback in user_feedbacks.find({"song":song_id}):
            status = user_feedback['status']
            feedbacks.append(status)

        limit = min(len(actions), len(feedbacks))
        for i in range(limit):
            date = actions[i][0]
            time = actions[i][1]
            temp = actions[i][2]
            weather = actions[i][3]
            feedback = feedbacks[i]
            action_data = [date, time, temp, weather, song_freq, feedback, user_id, song_id, song_genre]

            #pre-process the data
            action_data_normalized = preProcessData(action_data)
            actions_data.append(action_data_normalized)
    return actions_data


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
These are for testing
1. testFeedforwardCalc: recommendation part
2. testLearning: learning part
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def testFeedforwardCalc(user_id, param_NN):
    action_data = [0.33,0.62,0.29,0.72,0.12, 1.0, 0, 7, 5]
    input_data = action_data[:6]
    song_id = str(action_data[7])
    category_id = str(action_data[8])

    # calc network (this is for recommendation) 
    vec_category = main(user_id, input_data, param_NN)


def testLearning(user_id, param_NN):
    #action_data_i = ["day", "time", "temperature", "weather", "freqency", "feedback", "user_id", "song_id", "category_id"]
    actions_data = [
            [0.33,0.62,0.29,0.72,0.12, 1.0, 0, 7, 5],
            [0.45,0.22,0.74,0.12,0.72, 0.5, 0, 3, 8],
            [0.65,0.52,0.39,0.26,0.68, 0.0, 0, 2, 2],
            [0.45,0.22,0.74,0.12,0.72, 0.5, 0, 1, 7],
            [0.85,0.69,0.45,0.73,0.61, 0.5, 0, 9, 8],
            [0.25,0.50,0.19,0.99,0.28, 1.0, 0, 7, 5],
            [0.15,0.62,0.30,0.86,0.18, 0.0, 0, 4, 2]
            ]

    # learning (this is for learning network)
    learning_rate = 0.01
    NN = NeuralNetwork(user_id, param_NN[0], param_NN[1], param_NN[2], learning_rate)
    learningNetwork(user_id, actions_data, param_NN);




def checkInputData():
    #引数として、user_id をうけとる
    import sys
    argv = sys.argv
    argc = len(argv) #this should be 2 including argv[0](file_name)

    if argc == 1:
        print 'just testing this file'
        user_id = 0
    elif argc == 2:
        user_id = argv[1]
    else:
        print 'Something wrong with Input length'
        quit()
    return str(user_id)



def main(id_info, input_data, param_NN):
    #id_info = [user_id, song_id, category_id]
    user_id = id_info[0]
    learning_rate = 0.00
    NN = NeuralNetwork(user_id, param_NN[0], param_NN[1], param_NN[2], learning_rate)
    # the input value need to be considered. need minus value to expand difference of values after through sigmoid function
    output = NN.feedForward(input_data, weights='main')
    return output


def learningNetwork(user_id, actions_data, param_NN):
    #id_info = [user_id, song_id, category_id]
    #song_info = [str(actions_data[7]), str(actions_data[8])]
    
    learning_rate = 0.01
    NN = NeuralNetwork(user_id, param_NN[0], param_NN[1], param_NN[2], learning_rate)
    new_weights = NN.startLearning(actions_data)

    #process the new_weights to json style
    new_weights_json = NN.setWeights_JsonFormat(new_weights)
    # save weights
    NN.pullUptoFile(user_id, new_weights_json)


if __name__ == "__main__":
    #user_id : string
    user_id = checkInputData()
    param_NN = [6, 5, 10]
    #testFeedforwardCalc(user_id, param_NN)
    #testLearning(user_id, param_NN)

    #--------------------Learning -------------------------
    # get user actions from mongoDB
    actions_data = getUserActions(user_id)

    learning_rate = 0.01
    #init user's NeuralNetwork
    NN = NeuralNetwork(user_id, param_NN[0], param_NN[1], param_NN[2], learning_rate)
    #start learning
    learningNetwork(user_id, actions_data, param_NN);
    print 'SUCCESS'

