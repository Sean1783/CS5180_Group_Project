from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from project_indexer import clean_text, connect_database

class QueryProcessor:

    def query(self):
        query_string = "Salisbury"
        query_string = clean_text(query_string)
        vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3))
        query_vector = vectorizer.fit([query_string])
        ngrams = vectorizer.get_feature_names_out()

        db = connect_database('project_db')
        collection = db.v2_inverted_index

        hits = dict()
        for ngram in ngrams:
            result = collection.find_one({'term': ngram})
            if result:
                term = result['term']
                for doc in result['records']:
                    url = doc["url"]
                    score = doc["tfidf"]
                    if url in hits:
                        hits[url] += score
                    else:
                        hits[url] = score

        print(hits)

