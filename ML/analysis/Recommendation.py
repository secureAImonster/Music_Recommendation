# -*- coding: utf-8 -*-
def preProcessData(data):
    """ 
    data[0]: date(mm/dd/yyyy)
    data[1]: time(hh:mm:ss)
    data[2]: temperature 
    data[3]: weather 
    data[4]: frequency
    data[5]: feedback 
    don't use #data[6]: user_id 
    don't use #data[7]: song_id 
    don't use #data[8]: category_id 
    """
    result = []
    
    # --- date ---
    #don't care about year now...
    str_date = data[0]
    splited_date = str_date.split('/')
    month = float(splited_date[0])
    day = float(splited_date[1])
    # normalization roughly
    n_date = ((month - 1)*30 + day)/365
    result.append(n_date)

    # --- time ---
    str_time = data[1]
    splited_time = str_time.split(':')
    hour = float(splited_time[0])
    minute = float(splited_time[1])
    second = float(splited_time[2])
    # normalization 
    n_time = (hour*12 + minute * 60 + second)/60*60*24
    result.append(n_time)

    # --- temperature --- set as max:30
    str_temp = data[2]
    n_temp = float(str_temp)/30
    result.append(n_temp)

    # --- weather ---
    str_weather = float(data[3])
    result.append(str_weather)
    
    # --- frequency ---  This should be 0 when output recommendation
    result.append(float(data[4]))
    #str_freq = data[4]
    #n_freq = float(str_freq)/100
    #result.append(n_freq)

    # --- feedback --- This should be 0 when output recommendation
    result.append(float(data[5]))
    #str_fb = data[5]
    #n_fb = (float(str_fb)+50)/100
    #result.append(n_fb)

    if len(data) == 9:
        # --- user_id ---
        result.append(int(data[6]))
        # --- song_id ---
        result.append(int(data[7]))
        # --- category_id ---
        result.append(int(data[8]))
    
    return result 



def checkInputData():
    """ # check input data #
    input 1 (argv[1]): mm/dd/yyyy 
    input 2 (argv[2]): time
    input 3 (argv[3]): temperature 
    input 4 (argv[4]): weather 
    input 5 (argv[5]): frequency
    input 6 (argv[6]): feedback 
    input 7 (argv[7]): user_id
    don't use #input 8 (argv[8]): song_id
    don't use #input 9 (argv[9]): category_id 
    """
    import sys
    action_data = []
    argv = sys.argv
    argc = len(argv) #this should be 8 including argv[0](file_name)

    if argc == 1:
        print 'just testing this file'
        action_data = ["10/18/2015", "16:50:10", "25.60", "0.7", "1.00", "1.00"]
        id_info = ["0", "7", "5"] #id_info = [user_id, song_id, category_id]
    elif argc == 8:
        # new action
        action_data = [argv[1], argv[2], argv[3], argv[4], argv[5], argv[6]]
        id_info = [argv[7]]
    elif argc == 10:
        #learning
        action_data = [argv[1], argv[2], argv[3], argv[4], argv[5], argv[6]]
        id_info = [argv[7], argv[8], argv[9]]
    else:
        print 'Something wrong with Input length'
        quit()
    
    return id_info, action_data 


def main(id_info, input_data, param_NN):
    import NeuralNetwork
    import SelectMusic
    import numpy as np

    ### execute
    #1. calc category vector which shows the distribution of weights, which shows the user's like 
    user_id = id_info[0]
    category_vec = NeuralNetwork.main(user_id, input_data, param_NN)

    #2. Select music category and music 
    selectedMusic = SelectMusic.main(user_id, category_vec)
    
    # This stdout is sending to view page
    print selectedMusic
    return selectedMusic



if __name__ == "__main__":
    #checking the input data
    id_info, action_data = checkInputData()

    #pre-processing the data, normalization
    input_data = preProcessData(action_data)

    # Number of nodes in each layer: param_NN = [INPUT, HIDDEN, OUTPUT]
    param_NN = [6, 5, 10]
    main(id_info, input_data, param_NN)
