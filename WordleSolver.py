import csv

five_letter_words = []
ineligible_words = []
working_array = []
current_guess = ''
current_feedback = ''


def get_words():
    with open('FiveLetterWords.txt', 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            five_letter_words.append(row[0].upper())


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
    print("Removing all words that contain {0}".format(character))
    for word in five_letter_words:
        if character in word:
            ineligible_words.append(word)
    remove_ineligible_words()


def process_green_character(character, index):
    print("Removing all words that don't have {0} in index: {1}".format(character, index))
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

        if not is_phantom_feedback(currentCharacter, index):
            if characterFeedback == '_':
                process_nonexistent_character(currentCharacter)
            elif characterFeedback == 'G':
                process_green_character(currentCharacter, index)
            elif characterFeedback == 'Y':
                # print("processing yellow character")
                process_yellow_character(currentCharacter, index)
    eligible_words = [word for word in five_letter_words if word not in ineligible_words]
    return eligible_words


get_words()

current_guess = input('What is you first guess?\n').upper()
current_feedback = input('What was Wordle\'s feedback?\n').upper()

five_letter_words = process_all_feedback()
print('There are {0} eligible words left'.format(len(five_letter_words)))

while True:
    current_guess = five_letter_words[0].upper()
    print("Your guess should be {0}".format(current_guess))
    current_feedback = input('What was Wordle\'s feedback?\n').upper()
    five_letter_words = process_all_feedback()
    print('There are {0} eligible words left'.format(len(five_letter_words)))
