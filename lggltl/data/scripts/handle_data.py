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

def duplicate_data():
    return None


def run():
    train, test = split_train_test()
    print(test)

if __name__ == '__main__':
    #load_data()
    #clean_data()
    #duplicate_data()
    #train, test = split_train_test()
    run()

