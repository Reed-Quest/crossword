import numpy as np
import random

def find_shared_letter(word1,word2):
    shared_ls = []
    for letter in word1:
        if letter in word2:
            shared_ls.append(letter)
    return shared_ls

def count_shared_letters(word1,word2):
    shared_ls = find_shared_letter(word1,word2)
    return len(shared_ls)

def have_shared_letter(word1,word2):
    for letter in word1:
        if letter in word2:
            return True
    return False

def retrieve_tile_value(x,y):
    return grid[x][y]

def place_letter(letter,x,y):
    grid[x][y] = letter

def grid_bounds():
    x_ls = []
    y_ls = []
    for x in grid:
        x_ls.append(x)
        for y in grid[x]:
            y_ls.append(y)
    x_ls = np.unique(x_ls)
    y_ls = np.unique(y_ls)
    result = {}

    result['x'] = {}
    result['x']['max'] = max(x_ls)
    result['x']['min'] = min(x_ls)

    result['y'] = {}
    result['y']['max'] = max(y_ls)
    result['y']['min'] = min(y_ls)
    
    return result

def print_grid():
    bounds = grid_bounds()
    for y in range(bounds['y']['min'],bounds['y']['max']+1):
        for x in range(bounds['x']['min'],bounds['x']['max']+1):
            curr_value = grid[x][y]
            if curr_value != None:
                print(curr_value,end="")
            else:
                print('_',end="")
        print('\n')
    print('\n')
    print('END GRID')

def place_word(start_x,start_y,word,direction):
    curr_x = start_x
    curr_y = start_y

    if direction == "up":
        x_increment = 0
        y_increment = -1
    elif direction == "down":
        x_increment = 0
        y_increment = 1
    elif direction == "right":
        x_increment = 1
        y_increment = 0
    elif direction == "left":
        x_increment = -1
        y_increment = 0

    i = 0
    while i < len(word):
        place_letter(word[i],curr_x,curr_y)
        curr_x += x_increment
        curr_y += y_increment
        i += 1

    placed_words[word] = [start_x,start_y,direction]

def is_possible_placement(start_x,start_y,word,direction):
    success = True
    
    curr_x = start_x
    curr_y = start_y

    if direction == "up":
        x_increment = 0
        y_increment = -1
    elif direction == "down":
        x_increment = 0
        y_increment = 1
    elif direction == "right":
        x_increment = 1
        y_increment = 0
    elif direction == "left":
        x_increment = -1
        y_increment = 0

    i = 0
    while success and i < len(word):
        curr_tile = retrieve_tile_value(curr_x,curr_y)
        curr_letter = word[i]

        if direction == "right":
            border1 = retrieve_tile_value(curr_x,curr_y-1)
            border2 = retrieve_tile_value(curr_x,curr_y+1)
        else:
            border1 = retrieve_tile_value(curr_x-1,curr_y)
            border2 = retrieve_tile_value(curr_x+1,curr_y)
        
        if curr_tile != None:
            if curr_tile != curr_letter:
                success = False             
        else:
            if border1 != None or border2 != None:
                success = False

        curr_x += x_increment
        curr_y += y_increment
        i += 1

    return success

def find_letter_position(word,letter_index):
    start_x = placed_words[word][0]
    start_y = placed_words[word][1]
    direction = placed_words[word][2]
    if direction == "up":
        start_y -= letter_index
    elif direction == "down":
        start_y += letter_index
    elif direction == "right":
        start_x += letter_index
    elif direction == "left":
        start_x -= letter_index
    return [start_x,start_y]

def find_shared_indices(word1,word2):
    all_results = []
    for i in range(0,len(word1)):
        curr_letter_word1 = word1[i]
        for j in range(0,len(word2)):
            curr_letter_word2 = word2[j]
            if curr_letter_word1 == curr_letter_word2:
                curr_match = [i,j]
                all_results.append(curr_match)
    return all_results

def find_shared_coordinate(print_word,match_pair):
    coord = find_letter_position(print_word,match_pair[0])
    return coord

def select_shared_start_coordinate(print_word,hyp_word):
    possible_match_pairs = find_shared_indices(print_word,hyp_word)
    chosen_match_pair = random.choice(possible_match_pairs)
    chosen_coordinate = find_shared_coordinate(print_word,chosen_match_pair)

    print_direction = placed_words[print_word][2]

    if print_direction == "right":
        hyp_direction = "down"
    elif print_direction == "down":
        hyp_direction = "right"

    if hyp_direction == "right":
        chosen_coordinate[0] -= chosen_match_pair[1]
    else:
        chosen_coordinate[1] -= chosen_match_pair[1]

    return chosen_coordinate

def add_bound_word(print_word,hyp_word):

    print_direction = placed_words[print_word][2]

    if print_direction == "right":
        hyp_direction = "down"
    elif print_direction == "down":
        hyp_direction = "right"

    i = 0
    while i < 10:
        if have_shared_letter(print_word,hyp_word):
            start_coor = select_shared_start_coordinate(print_word,hyp_word)
            is_possible = is_possible_placement(start_coor[0],start_coor[1],hyp_word,hyp_direction)
            if is_possible:
                place_word(start_coor[0],start_coor[1],hyp_word,hyp_direction)
                return True
        i += 1

    return False

def get_all_placed_words():
    ls = []
    for k in placed_words:
        ls.append(k)
    return(ls)

def count_possible_connections(word,words_ls):
    possible_connections_count = 0
    for x in words_ls:
        if x != word:
            possible_connections_count += count_shared_letters(word,x)
    return possible_connections_count

def get_word_lowest_connection_count(candidates,words_ls):
    candidate_word = candidates[0]
    candidate_count = count_possible_connections(candidate_word,words_ls)
    for curr_word in candidates:
        curr_count = count_possible_connections(curr_word,words_ls)
        if curr_count < candidate_count:
            candidate_word = curr_word
            candidate_count = curr_count
    return candidate_word

def sort_list_by_connections(all_words_ls):
    result_ls = []
    candidate_ls = all_words_ls.copy()
    while len(candidate_ls) > 0:
        curr_word = get_word_lowest_connection_count(candidate_ls,all_words_ls)
        result_ls.append(curr_word)
        candidate_ls.remove(curr_word)
    return result_ls

def calculate_success_rate():
    all_placed_words = get_all_placed_words()
    all_words_overall = words_ls.copy()
    success_rate = len(all_placed_words) / len(all_words_overall)
    return success_rate

words_ls = ['doyleowl','bagels','scrounge','blue like jazz','moss','geese','woodstock','kommie','balls','library','gary','eliot hall','cherry blossoms','psychology','noise parade']

success_rate = 0
j = 0

while j < 100 and success_rate < 1:
    sorted_words_ls = sort_list_by_connections(words_ls)

    grid = {}
    placed_words = {}

    for x in range(-50,50):
        grid[x] = {}
        for y in range(-50,50):
            grid[x][y] = None

    first_word = random.choice(sorted_words_ls)

    place_word(0,0,first_word,random.choice(['right','down']))
    sorted_words_ls.remove(first_word)

    while len(sorted_words_ls) > 0:
        curr_word = random.choice(sorted_words_ls)
        all_placed_words = get_all_placed_words()
        
        success = False
        i = 0
        while not success and i < 100:
            curr_bind = random.choice(all_placed_words)
            success = add_bound_word(curr_bind,curr_word)
            i += 1
        sorted_words_ls.remove(curr_word)
    
    success_rate = calculate_success_rate()
    j += 1

print_grid()

all_placed_words = get_all_placed_words()
print("Success Rate:",end="\t")
print(str(len(all_placed_words)),"/",str(len(words_ls)))




