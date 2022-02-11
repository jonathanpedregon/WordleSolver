import csv

five_letter_words = []
ineligible_words = []
current_guess = ''
current_feedback = ''


def get_words():
    with open('FiveLetterWords.txt', 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            five_letter_words.append(row[0].upper())


def get_remaining_characters():
    return "".join(five_letter_words)


def get_character_counts():
    character_string = get_remaining_characters()
    count_dictionary = {}
    for character in sorted(set(character_string)):
        character_count = character_string.count(character)
        count_dictionary[character] = character_count
    return count_dictionary


def get_word_scores():
    word_scores = {}
    character_counts = get_character_counts()
    for word in five_letter_words:
        word_score = 0
        for character in set(word):
            # maybe remove the set?
            word_score += character_counts[character]
        word_scores[word] = word_score

    return word_scores


def get_next_word():
    word_scores = get_word_scores()
    next_word = max(word_scores, key = lambda x: word_scores[x])
    return next_word


def remove_ineligible_words():
    for ineligible_word in ineligible_words:
        five_letter_words.remove(ineligible_word)
    ineligible_words.clear()


def find_indices_of_char(character):
    indices = []
    for index in range(5):
        if character == current_guess[index]:
            indices.append(index)
    return indices


def removeDupWithoutOrder(string):
    return "".join(set(string))


def is_phantom_feedback(character, index):
    character_indices = find_indices_of_char(character)

    if len(character_indices) == 1:
        return False

    character_feedback = current_feedback[index]
    if character_feedback != '_':
        return False

    for character_index in character_indices:
        if character_index == index:
            continue
        other_feedback = current_feedback[character_index]
        if other_feedback == 'G' or other_feedback == 'Y':
            return True

    return False


def process_nonexistent_character(character):
    for word in five_letter_words:
        if character in word:
            ineligible_words.append(word)
    remove_ineligible_words()


def process_green_character(character, index):
    for word in five_letter_words:
        comparison_character = word[index]
        if comparison_character != character:
            ineligible_words.append(word)
    remove_ineligible_words()


def process_yellow_character(character, index):
    for word in five_letter_words:
        if word[index].upper() == character.upper():
            ineligible_words.append(word)

    for word in five_letter_words:
        if character.upper() not in word.upper():
            ineligible_words.append(word)
    remove_ineligible_words()


def process_all_feedback():
    for index in range(5):
        currentCharacter = current_guess[index].upper()
        characterFeedback = current_feedback[index].upper()

        if is_phantom_feedback(currentCharacter, index):
            characterFeedback = 'Y'
        if characterFeedback == '_':
            process_nonexistent_character(currentCharacter)
        elif characterFeedback == 'G':
            process_green_character(currentCharacter, index)
        elif characterFeedback == 'Y':
            process_yellow_character(currentCharacter, index)
    eligible_words = [word for word in five_letter_words if word not in ineligible_words]
    return eligible_words


get_words()

current_guess = get_next_word()
print('Your first guess should be {0}\n'.format(current_guess))
current_feedback = input('What was Wordle\'s feedback?\n').upper()

five_letter_words = process_all_feedback()
print('There are {0} eligible words left'.format(len(five_letter_words)))

while True:
    current_guess = get_next_word().upper()
    print("Your guess should be {0}".format(current_guess))
    current_feedback = input('What was Wordle\'s feedback?\n').upper()
    five_letter_words = process_all_feedback()
    print('There are {0} eligible words left'.format(len(five_letter_words)))
