import math

from nltk import ngrams

from utilities import clean_text, connect_database

class QueryProcessor:

    def make_n_grams(self, cleaned_text, n):
        consolidated_n_grams = list()
        for i in range(1, n+1):
            n_grams = ngrams(cleaned_text.split(), i)
            for gram in n_grams:
                joined_string = ' '.join(gram)
                consolidated_n_grams.append(joined_string)
        return consolidated_n_grams


    def generate_term_frequency_pair(self, n_grams, cleaned_string):
        query_vector = list()
        total_word_count = len(cleaned_string.split())
        for gram in n_grams:
            element = dict()
            count = cleaned_string.count(gram)
            term_frequency = count / (total_word_count/len(gram.split()))
            element['term'] = gram
            element['tf'] = term_frequency
            query_vector.append(element)
        return query_vector


    def rank_result(self, link_score_map):
        if len(link_score_map) > 0:
            result_length = len(link_score_map)
            sorted_dict = sorted(link_score_map.items(), key=lambda item: item[1], reverse=True)
            if result_length > 5:
                return sorted_dict[:5]
            else:
                return sorted_dict[:result_length]
        return None


    def get_magnitude_of_doc_vector(self, doc_vector):
        value = 0
        for element in doc_vector:
            if 'tfidf' in element:
                value = value + element['tfidf']**2
            elif 'tf' in element:
                value = value + element['tf']**2
        return math.sqrt(value)


    def query_v2(self, query_string):
        cleaned_string = clean_text(query_string)
        n_grams = self.make_n_grams(cleaned_string, 3)
        query_vector = self.generate_term_frequency_pair(n_grams, cleaned_string)
        db = connect_database('project_db')
        collection = db.v2_inverted_index
        hits = dict()
        query_magnitude =  self.get_magnitude_of_doc_vector(query_vector)
        for n_gram_term in query_vector:
            result = collection.find_one({'term': n_gram_term['term']})
            if result is not None:
                doc_magnitude = self.get_magnitude_of_doc_vector(result['records'])
                product_of_magnitude = doc_magnitude * query_magnitude
                for doc in result['records']:
                    url = doc['url']
                    score = doc['tfidf'] * (n_gram_term['tf'] * result['idf'])
                    normalized_score = score / product_of_magnitude if product_of_magnitude != 0 else 0
                    if url in hits:
                        hits[url] += normalized_score
                    else:
                        hits[url] = normalized_score
        return hits
