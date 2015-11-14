#-*- coding:utf-8 -*-
import numpy as np
class Recsys:

    """
    Input: Vector of movie category (the sum of each wise is 1)
    Output: Category & Music

    -flow-
    1. chose the max value element and its number from the vector
    2. calculate 'evaluation' vector which is the use's value for each music.
    3. chose top X from that vector
    4. chose 1 from the top X randomly
    """

    def __init__(self, category_vec):
        self.category_vec = category_vec

    def calcWeightRatio(self, user_table):
        #weight ratio (weight of feedback/weight of freq)
        #user_table = user_table[0]
        weight_ratios = np.ones(len(user_table))
        for i in range(len(user_table)):
            #freq = int(user_table[i][2])
            freq = user_table[i][2]
            if freq > 20:
                weight_ratios[i] = 3
            elif freq > 15 and freq <= 20:
                weight_ratios[i] = 2
            elif freq > 10 and freq <= 15:
                weight_ratios[i] = 1
            elif freq > 5 and freq <= 10:
                weight_ratios[i] = 2
            elif freq <= 5:
                weight_ratios[i] = 3
            else:
                weight_ratios[i] = 1
        return weight_ratios


    def evalMusic(self, user_table, weight_ratios):
        #splited_arrays = np.dsplit(user_table, 3)
        #music, category, freq, feedback = splited_arrays[0], splited_arrays[1], splited_arrays[2], splited_arrays[3]
        evaluated_table = []
        #user_table = user_table[0]

        category_id = user_table[0][1]
        for i in range(len(user_table)):
            song_id = user_table[i][0]
            freq = user_table[i][2]
            feedback = user_table[i][3]
            ratio = weight_ratios[i]
            #evaluated_vec[i] = int(freq) + int(feedback) * ratio
            evaluated_value = freq + feedback * ratio
            evaluated_table.append([song_id, category_id, evaluated_value])

        return evaluated_table


    def choseTopX(self, vector, num_X):
        result = []
        indexs = sorted(range(len(vector)), key=lambda i: vector[i][2])[-num_X:]
        for index in indexs:
            result.append(vector[index])
        return result



    def indexOfMaxValue(self, vector):
        max_value = max(vector)
        str_vector = map(str,vector)
        index = str_vector.index(str(max_value))
        return index


def makeTestUserTable():
    num_of_music_user_has = 50
    # song, category, freq, feedback 
    # ex. [["music1", "category3", 3, 2], ["music2", "category6", 2, 1], ..., ["music50", "category4", 6, 4]]
    music = np.array(["music"+str(i) for i in range(num_of_music_user_has)])
    category = np.array(["category"+str(int(np.random.random()*10)) for i in range(num_of_music_user_has)])
    freq = np.array(np.random.randint(0,30, num_of_music_user_has))
    feedback = np.array(np.random.randint(-10, 10, num_of_music_user_has))
    user_table = np.dstack((music, category, freq, feedback))
    return user_table

def makeUserTable(user_id, category_index):
    """ 
    pull down user's songs from mongo db
    and filtering by category_index
    >> input: user_id, category_index
    """
    user_table = []
    user_id = int(user_id)

    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    # connect to db 'prefy'
    db = client.prefy
    #get collection
    user_songs = db.songs
    song_feedbacks = db.feedbacks

    for song_info in user_songs.find({"user": user_id, "genre": category_index}):
        song_id = song_info['_id']
        song_genre = song_info['genre'] 
        song_freq = song_info['playtimes']

        song_sum_feedbacks = 0
        for feedback_info in song_feedbacks.find({"song":song_id}):
            status = feedback_info['status']
            song_sum_feedbacks += status

        song_vec = [song_id, song_genre, song_freq, song_sum_feedbacks]
        user_table.append(song_vec)
    return np.array(user_table)


def main(user_id, category_vector):
    num_of_category = len(category_vector)
    #normalization to 1
    category_vec = category_vector / sum(category_vector)

    Sys = Recsys(category_vec)

    #1. chose the max value element and its number from the vector
    category_index = Sys.indexOfMaxValue(category_vec)
    #print 'Category is ...' + str(category_index)

    # calculate weight ratio for each music
    #user_table = makeTestUserTable()
    user_table = makeUserTable(user_id, category_index)
    weight_ratios = Sys.calcWeightRatio(user_table)

    #2. calculate 'evaluation' vector which is the use's value for each music.
    evaluated_table = Sys.evalMusic(user_table, weight_ratios)
    
    #3. chose top X from that vector
    num_X = 5
    topX_vec = Sys.choseTopX(evaluated_table, num_X)
    
    #chose one from topX_vec
    XYZ = np.random.randint(0, num_X)
    recommended_music = topX_vec[XYZ]
    #print 'Your music recommended is No.' + str(recommended_music)
    music_id = recommended_music[0]
    return music_id
    

if __name__ == "__main__":
    import sys
    user_id = 0
    category_vector = np.random.random(10)
    sys.exit(main(user_id, category_vector))
    
