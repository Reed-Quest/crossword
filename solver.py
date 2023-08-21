import numpy as np
import random

def find_shared_letter(word1,word2):
    shared_ls = []
    for letter in word1:
        if letter in word2:
            shared_ls.append(letter)
    return shared_ls

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
    while i < len(word):
        curr_tile = retrieve_tile_value(curr_x,curr_y)
        curr_letter = word[i]
        
        if curr_tile != None and curr_tile != curr_letter:
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
        start_coor = select_shared_start_coordinate(print_word,hyp_word)
        is_possible = is_possible_placement(start_coor[0],start_coor[1],hyp_word,hyp_direction)
        if is_possible:
            place_word(start_coor[0],start_coor[1],hyp_word,hyp_direction)
            return True

    return False

def get_all_placed_words():
    ls = []
    for k in placed_words:
        ls.append(k)
    return(ls)

class coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

words_ls = ['magneto','vader','gorn']

grid = {}
placed_words = {}

for x in range(-50,50):
    grid[x] = {}
    for y in range(-50,50):
        grid[x][y] = None

first_word = random.choice(words_ls)

place_word(0,0,first_word,random.choice(['right','down']))
words_ls.remove(first_word)

while len(words_ls) > 0:
    curr_word = random.choice(words_ls)
    all_placed_words = get_all_placed_words()
    
    success = False
    i = 0
    while not success and i < 10:
        curr_bind = random.choice(all_placed_words)
        success = add_bound_word(curr_bind,curr_word)
        i += 1
    words_ls.remove(curr_word)

print_grid()




