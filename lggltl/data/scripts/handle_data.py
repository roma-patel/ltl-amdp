import json, os
import nltk
import re
import numpy as np

def load_data():
    fname = '/Users/romapatel/Downloads/AMT_results_annotated.tsv'
    f = open(fname, 'r')
    lines = [line.strip().split('\t') for line in f.readlines()]

    fname_lang = 'hard_pc_src_syn2.txt'
    fname_ltl = 'hard_pc_tar_syn2.txt'

    flang = open(os.getcwd() + '/' + fname_lang, 'w+')
    fltl = open(os.getcwd() + '/' + fname_ltl, 'w+')

    items = []
    for line in lines[1:]:
        if len(line) < 2: continue
        #if line[-1] == '0':
            #print(line)
            #continue
        words = nltk.word_tokenize(line[0].lower()) 
        ltl = re.sub('\(', ' ( ', line[1])
        ltl = re.sub('\)', ' ) ', ltl)
        ltl = [item for item in ltl.split(' ') if len(item) > 0]


        words_s = ' '.join(item for item in words)
        ltl_s = ' '.join(item for item in ltl)

        items.append([words_s, ltl_s])
        flang.write(words_s + '\n')
        fltl.write(ltl_s + '\n')

    print(len(items))

def split_train_test():
    fname_lang = 'hard_pc_src_syn2.txt'
    fname_ltl = 'hard_pc_tar_syn2.txt'

    flang = open(os.getcwd() + '/' + fname_lang, 'r')
    fltl = open(os.getcwd() + '/' + fname_ltl, 'r')

    lang_lines = [item.strip() for item in flang.readlines()]
    ltl_lines = [item.strip() for item in fltl.readlines()]

    ltl_dict = {item : [] for item in list(set(ltl_lines))}

    for i in range(len(ltl_lines)):
        ltl_dict[ltl_lines[i]].append(lang_lines[i])


    # split randomly
    total = len(lang_lines)
    items = [[lang_lines[i], ltl_lines[i]] for i in range(total)]
    np.random.shuffle(items)
    test = items[:round(0.2*total)]
    train = items[round(0.2*total):]
    print('Length test: ', len(test))
    print('Length train: ', len(train))


    # hold out 5 LTL commands (20%)



    return train, test

# mostly done in load_data with annotated file
def clean_data():
    fname = '/Users/romapatel/Downloads/AMT_results_annotated.tsv'
    f = open(fname, 'r')
    lines = [line.strip().split('\t') for line in f.readlines()]

    fname_lang = 'hard_pc_src_syn2.txt'
    fname_ltl = 'hard_pc_tar_syn2.txt'

    flang = open(os.getcwd() + '/' + fname_lang, 'w+')
    fltl = open(os.getcwd() + '/' + fname_ltl, 'w+')

    items = []
    for line in lines[1:]:
        if len(line) < 2: continue
        if line[-1] == '0':
            print(line)
            continue
        words = nltk.word_tokenize(line[0].lower())
        ltl = re.sub('\(', ' ( ', line[1])
        ltl = re.sub('\)', ' ) ', ltl)
        ltl = [item for item in ltl.split(' ') if len(item) > 0]


        words_s = ' '.join(item for item in words)
        ltl_s = ' '.join(item for item in ltl)

        items.append([words_s, ltl_s])
        flang.write(words_s + '\n')
        fltl.write(ltl_s + '\n')

    print(len(items))
    return None

def old_duplicate_data():
    fname_lang = 'hard_pc_src_syn2.txt'
    fname_ltl = 'hard_pc_tar_syn2.txt'

    flang = open(os.getcwd() + '/' + fname_lang, 'r')
    fltl = open(os.getcwd() + '/' + fname_ltl, 'r')

    lang_lines = [line.strip() for line in flang.readlines()]
    ltl_lines = [line.strip() for line in fltl.readlines()]

    floors = ['first_floor', 'second_floor', 'third_floor']
    landmarks = ['landmark_1', 'landmark_2', 'landmark_3']
    rooms = ['green_room', 'red_room', 'blue_room', 'purple_room', \
             'orange_room', 'yellow_room']

    ltl_keywords = floors + landmarks + rooms
    lang_keywords = [' '.join(item for item in keyword.split('_')) for keyword in ltl_keywords]

    lang_dup, ltl_dup = [], []

    #lang_lines = lang_lines[:10]
    items = []




    #lang_lines = lang_lines[:1]
    for i in range(len(lang_lines)):
        indicators = 0
        print('\nNew')
        lang, ltl = lang_lines[i], ltl_lines[i]
        print(lang, ltl); print()


        for floor in floors:
            floor_str = ' '.join(item for item in floor.split('_'))
            if floor_str not in lang:
                #items.append(lang_str + '\n' + ltl_str)
                #print('No floor!')
                continue
            # this floor is in here
            #print('Floor!')
            for other_floor in floors:
                other_floor_str = ' '.join(item for item in other_floor.split('_'))
                #if floor_str == other_floor_str: continue

                lang_str = re.sub(floor_str, other_floor_str, lang)
                ltl_str = re.sub(floor, other_floor, ltl)
                if ltl_str.count(floor) > 1: continue
                if ltl_str.count(other_floor) > 1: continue

                items.append(lang_str + '\n' + ltl_str)

        for floor in landmarks:
            floor_str = ' '.join(item for item in floor.split('_'))
            if floor_str not in lang:
                #items.append([lang, ltl])
                #print('No landmark!')
                continue
            # this floor is in here
            #print('Landmark!')
            for other_floor in landmarks:
                other_floor_str = ' '.join(item for item in other_floor.split('_'))
                #if floor_str == other_floor_str: continue
                lang_str = re.sub(floor_str, other_floor_str, lang)
                ltl_str = re.sub(floor, other_floor, ltl)
                #ltl_props = ltl_str.split(' ')
                if ltl_str.count(floor) > 1: continue
                if ltl_str.count(other_floor) > 1: continue

                items.append(lang_str + '\n' + ltl_str)

        for floor in rooms:
            floor_str = ' '.join(item for item in floor.split('_'))
            if floor_str not in lang:
                #items.append([lang, ltl])
                #print('No landmark!')
                continue
            # this floor is in here
            #print('Landmark!')
            for other_floor in rooms:
                other_floor_str = ' '.join(item for item in other_floor.split('_'))
                #if floor_str == other_floor_str: continue

                lang_str = re.sub(floor_str, other_floor_str, lang)
                ltl_str = re.sub(floor, other_floor, ltl)
                if ltl_str.count(floor) > 1: continue
                if ltl_str.count(other_floor) > 1: continue

                items.append(lang_str + '\n' + ltl_str)


        #words = nltk.word_tokenize(line[0].lower())
        #print(words)


    items = list(set(items))
    for item in items:

        lang_dup.append(item.split('\n')[0])
        ltl_dup.append(item.split('\n')[1])

        print(item)


    print(len(lang_lines))
    print(len(items))


    #return

    fname_lang = 'hard_pc_src_syn2_dup.txt'
    fname_ltl = 'hard_pc_tar_syn2_dup.txt'

    flang = open(os.getcwd() + '/' + fname_lang, 'w+')
    fltl = open(os.getcwd() + '/' + fname_ltl, 'w+')

    for i in range(len(lang_dup)):
        flang.write(lang_dup[i] + '\n')
        fltl.write(ltl_dup[i] + '\n')

    return None

def duplicate_data():
    fname_lang = 'hard_pc_src_syn2.txt'
    fname_ltl = 'hard_pc_tar_syn2.txt'

    flang = open(os.getcwd() + '/' + fname_lang, 'r')
    fltl = open(os.getcwd() + '/' + fname_ltl, 'r')

    lang_lines = [line.strip() for line in flang.readlines()]
    ltl_lines = [line.strip() for line in fltl.readlines()]

    floors = ['first_floor', 'second_floor', 'third_floor']
    landmarks = ['landmark_1', 'landmark_2', 'landmark_3']
    rooms = ['green_room', 'red_room', 'blue_room', 'purple_room', \
             'orange_room', 'yellow_room']

    ltl_keywords = floors + landmarks + rooms
    lang_keywords = [' '.join(item for item in keyword.split('_')) for keyword in ltl_keywords]

    lang_dup, ltl_dup = [], []

    #lang_lines = lang_lines[:10]
    items = []

    def find_list(keyword, floors, landmarks, rooms):
        if keyword in floors:
            return floors
        elif keyword in landmarks:
            return landmarks
        elif keyword in rooms:
            return rooms
        else:
            return None


    import itertools

    items = []
    for i in range(len(lang_lines)):
        lang, ltl = lang_lines[i], ltl_lines[i]
        print('\nNew'); print(lang, ltl); print()
        keywords = [keyword for keyword in ltl_keywords if keyword in ltl]
        lang_keywords = [' '.join(item for item in keyword.split('_')) for keyword in keywords]
        if len(keywords) == 1:
            continue
        else:
            list_1 = find_list(keywords[0], floors, landmarks, rooms)
            list_2 = find_list(keywords[1], floors, landmarks, rooms)

            if list_1 == None or list_2 == None:
                items.append(lang + '\n' + ltl)
            for item in itertools.product(list_1, list_2):
                ltl_dup = re.sub(keywords[0], item[0], ltl)
                lang_dup = re.sub(lang_keywords[0], ' '.join(item for item in item[0].split('_')), ltl)






    items = list(set(items))
    for item in items:
        print(item)


    print(len(lang_lines))
    print(len(items))
    return

    fname_lang = 'hard_pc_src_syn2_dup.txt'
    fname_ltl = 'hard_pc_tar_syn2_dup.txt'

    flang = open(os.getcwd() + '/' + fname_lang, 'w+')
    fltl = open(os.getcwd() + '/' + fname_ltl, 'w+')

    for i in range(len(lang_dup)):
        fname_lang.write(lang_dup[i] + '\n')
        fname_ltl.write(ltl_dup[i] + '\n')

    return None


def run():
    train, test = split_train_test()
    print(test)

if __name__ == '__main__':
    #load_data()
    #clean_data()
    old_duplicate_data()
    #duplicate_data()

    #train, test = split_train_test()
    #run()

