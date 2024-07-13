import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import requests
import matplotlib.pyplot as plt

# Function to fetch text from the URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching text: {e}")
        return None

# Function to remove punctuation from text
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# Function to map words to (word, 1)
def map_function(word):
    return word.lower(), 1  # Convert word to lowercase for normalization

# Function to shuffle mapped values
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Function to reduce (word, counts) pairs
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Function to perform MapReduce on text
def map_reduce(text, search_words=None):
    # Remove punctuation
    text = remove_punctuation(text)
    words = text.split()

    # If search_words are provided, filter words
    if search_words:
        words = [word for word in words if word.lower() in search_words]

    # Parallel mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Shuffle step
    shuffled_values = shuffle_function(mapped_values)

    # Parallel reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    # Sort results by count
    sorted_results = sorted(reduced_values, key=lambda x: x[1], reverse=True)

    return dict(sorted_results)

# Function to visualize top words
def visualize_top_words(word_counts, top_n=10):
    top_words = list(word_counts.items())[:top_n]
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    # Input text URL
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Perform MapReduce on the input text
        result = map_reduce(text)

        # Print top 10 words
        top_10_words = list(result.items())[:10]
        print("Top 10 most frequent words:")
        for word, count in top_10_words:
            print(f"{word}: {count}")

        # Visualize results
        visualize_top_words(result)
    else:
        print("Error: Failed to fetch input text.")

