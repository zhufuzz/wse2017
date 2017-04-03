import urllib2
import string


class PageData:
    # page, rank, unique words, word positions, page found on
    def __init__(self, url, rank, unique_words_count, word_positions, word_found):
        self.url = url
        self.rank = rank
        self.unique_words_count = unique_words_count
        self.word_positions = word_positions
        self.words_found = [word_found, ]

    def get_url(self):
        return self.url

    def get_rank(self):
        return self.rank

    def get_unique_words_count(self):
        return self.unique_words_count

    def get_word_positions(self):
        return self.word_positions

    def get_words_found(self):
        return self.words_found

    def add_one_more_search_word(self, search_word, word_positions):
        self.word_positions.extend(word_positions)
        self.words_found.append(search_word)
        self.unique_words_count += 1


class SearchData:
    def __init__(self, num_search_words):
        self.all_words_match = []
        self.some_words_match = []
        self.single_words_match = []
        self.num_search_words = num_search_words

    def add_matching_page(self, page_data):
        if page_data.get_unique_words_count() == self.num_search_words:
            self.all_words_match.append((page_data.get_url(), page_data.get_rank(), page_data.get_words_found()))
        elif page_data.get_unique_words_count() > 1:
            self.some_words_match.append((page_data.get_url(), page_data.get_rank(), page_data.get_words_found()))
        elif page_data.get_unique_words_count() == 1:
            self.single_words_match.append((page_data.get_url(), page_data.get_rank(), page_data.get_words_found()))

    def get_ranked_matches(self):
        self.all_words_match = sorted(self.all_words_match, reverse=True,
                                      key=lambda x: x[1])  # sort by rank which is key 1
        self.some_words_match = sorted(self.some_words_match, reverse=True, key=lambda x: x[1])
        self.single_words_match = sorted(self.single_words_match, reverse=True, key=lambda x: x[1])

        # at this point we have everything sorted we just need to merge them now
        results = self.all_words_match
        results.extend(self.some_words_match)
        results.extend(self.single_words_match)

        return results


def print_search_engine_results(results):
    if len(results) > 0:
        for result in results:
            print(("\nURL: {0} \nRank: {1} \nMatched Words: {2}").format(result[0], result[1], result[2]))
            print ("Description text: ")
            description_result(result[0], result[2])
    else:
        print("\nNo results found")


def description_result(url, matched_words):
    response = urllib2.urlopen(url)
    html = response.read()
    html = html.strip(string.punctuation).split("\n")

    for line in html:
        line = line.lower().split(" ")
        for word in matched_words:
            if word in line:
                # find, get length of line and then substring
                pos = line.index(word)
                description_result_validation_check(pos - 1, line)
                description_result_validation_check(pos, line)
                description_result_validation_check(pos + 1, line)
                print ("")


def description_result_validation_check(pos, line):
    if pos > 0 and pos < len(line):
        word = line[pos]
        if word.find("<") == -1:
            print word,


def search(user_query_list, url_page_rank, word_index_data):
    search_engine_data = {}

    for search_word in user_query_list:

        if search_word in word_index_data:
            second_dict_of_index = word_index_data[search_word]

            for url in second_dict_of_index:
                word_positions = second_dict_of_index[url]
                page_rank = url_page_rank[url]

                if url in search_engine_data:
                    # handle if already present
                    url_data = search_engine_data[url]
                    url_data.add_one_more_search_word(search_word, word_positions)

                else:
                    url_data = PageData(url, page_rank, 1, word_positions, search_word)
                    search_engine_data[url] = url_data

    search_results = SearchData(len(user_query_list))
    for url in search_engine_data:
        search_results.add_matching_page(search_engine_data[url])

    results = search_results.get_ranked_matches()
    print_search_engine_results(results)
