from .classify import *
import json
import requests
from bs4 import BeautifulSoup

# based on: https://github.com/jaminthorns/spam-classifier

def is_bayes_safe(contents):
    config = json.load(open("config.json"))
    
    filename = "mytest/test.txt"
    soup = BeautifulSoup(contents, "html")
    for script in soup(["script", "style"]):
        script.decompose()
        
    text = soup.get_text()
    
    with open(filename, 'w') as outfile:
        outfile.write(text)
    
    spam_examples_folder = "spam_examples"
    ham_examples_folder = "ham_examples"
    spam_test_folder = "mytest"
    ham_test_folder = "mytest"
    
    init_prob_spam = config["system"]["bayes"]["init_prob_spam"]
    occurence_threshold = config["system"]["bayes"]["occurence_threshold"]
    score_threshold = config["system"]["bayes"]["score_threshold"]
    phrase_length = config["system"]["bayes"]["phrase_length"]
    
    spam_example_messages = get_messages(spam_examples_folder)
    ham_example_messages = get_messages(ham_examples_folder)
    spam_test_messages = get_messages(spam_test_folder)
    ham_test_messages = get_messages(ham_test_folder)
    
    spam_words = get_word_occurences(spam_example_messages, phrase_length)
    ham_words = get_word_occurences(ham_example_messages, phrase_length)
    spam_test_words = get_word_occurences(spam_test_messages, phrase_length)
    ham_test_words = get_word_occurences(ham_test_messages, phrase_length)
    
    spam_word_frequencies = get_word_frequencies(spam_words)
    ham_word_frequencies = get_word_frequencies(ham_words)
    
    word_spamicities = get_word_spamicities(spam_word_frequencies, ham_word_frequencies, init_prob_spam, occurence_threshold)
    
    spam_successes = 0
    ham_successes = 0
    
    for key in sorted(spam_test_words):
        message_score = get_spam_score(spam_test_words[key], word_spamicities)
        if message_score > score_threshold:
            spam_successes += 1
    
    for key in sorted(ham_test_words):
        message_score = get_spam_score(ham_test_words[key], word_spamicities)
        if message_score < score_threshold:
            ham_successes += 1
    
    spam_success_rate = spam_successes / len(spam_test_messages)
    ham_success_rate = ham_successes / len(ham_test_messages)
    
    if ham_success_rate > spam_success_rate:
        return False
    else:
        return True