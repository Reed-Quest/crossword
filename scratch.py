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
        print(curr_bind,curr_word)
        success = add_bound_word(curr_bind,curr_word)
        i += 1
    words_ls.remove(curr_word)

print(first_word)