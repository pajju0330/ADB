# Vaishnavi Ladda PRN:21610076
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import math

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    words = word_tokenize(text.lower())
    
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    
    return filtered_words

def compute_cosine_similarity(doc1, doc2):
    # Preprocess the documents
    tokens1 = preprocess_text(doc1)
    tokens2 = preprocess_text(doc2)
    
    # Create word frequency vectors
    vec1 = Counter(tokens1)
    vec2 = Counter(tokens2)
    
    # Compute dot product
    dot_product = sum(vec1[word] * vec2[word] for word in vec1 if word in vec2)

    # Compute magnitudes
    magnitude1 = math.sqrt(sum(vec1[word] ** 2 for word in vec1))
    magnitude2 = math.sqrt(sum(vec2[word] ** 2 for word in vec2))
    
    similarity = dot_product / (magnitude1 * magnitude2) if magnitude1 != 0 and magnitude2 != 0 else 0.0
    
    return similarity

# Example usage
with open('test1.txt', 'r') as file:
    text = file.read()
    document1 = text

with open('test2.txt', 'r') as file:
    text = file.read()
    document2 = text

similarity = compute_cosine_similarity(document1, document2)
print(f"Similarity between the documents: {similarity:.2f}")
