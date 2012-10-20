"""
This will take up a list of keywords as argument and return a list of all keywords which can be built using thesaurus.
"""
try:
    import argparse
except ImportError:
    # Not python 2.7
    import optparse
import copy
from nltk.corpus import wordnet as wn
from odict import odict

word_dict = {}
kwd_list = []


class MainThesaurusHandler():
    """Class for Creating thesaurus Handler."""

    def __init__(self, exist_kwds, config):
        """Constructor.
        Args:
            exist_kwds: A list of source/sample words.
            # TODO(mrafi): Change config from a dictionary to depth level.
            config: a dictionary containing flags for hypernymns and hyponymns."""
        self.ekwds = self.make_list(exist_kwds)
        self.config = config  # config is a dictionary
        self.nkwds = []
        self.word_dict = odict()
        self.filex = 'test.txt'
        self.kwd_list = []
        self.final_word_dict = odict()

    def make_list(cls, kwds):
        kwd_list = []
        temp = kwds
        for i in temp:
            kwd_list.append(i)
        return kwd_list

    def add(self,):
        pass

    def permuterex(self, items, suffix, n):
        """Permutes over 2 given lists."""
        #items is a list of tuples
        if n + 1 == len(items):
            last = True
        else:
            last = False
        x = len(items[n])
        for i in xrange(x):
            self.word_dict[n] = items[n][i]
            if last == False:
                self.permuterex(items, suffix, n + 1)
            if last == True:
                tt = ''
                for x in self.word_dict.values():
                    tt += ' ' + str(x)  # added space for no space errors
                self.kwd_list.append(tt.strip())

    def get_negative_keywords(self, neg_kwds, synset):
        negative_keywords = []
        for negate in neg_kwds:
            if negate.lower() in synset.lemma_names:
                negative_keywords.append(synset)
            #for each negative kwd
            #find its synset
            #for each of its synset...find the distance b/w
            negatex = wn.synsets(negate)
            if negatex:
                for xxx in negatex:
                    t = xxx.wup_similarity(synset)
                    if t > 0.6:
                        negative_keywords.append(synset)
                        break

        return negative_keywords

    def generate_thesaurus(self, neg_kwds):
        """The main function which gets thesaurus keywords.

        Loops through existing keywords and get
        thesaurus keywords based on config.

        Args:
            neg_kwds: a list of keywords whose context related keywords
                      should not be included.
        Returns:
            A dictionary containing """
        ekwds = self.ekwds  # existing keywords.
        synsxx = odict()  # Ordered dictionary.
        for kwd in ekwds:
            # do this for each word in a kwd
            s_kwd = kwd.split()
            synsxx[kwd] = odict()  # ([],[]) #close syns and hyponyms
            for x in s_kwd:
                synsxx[kwd][x] = [[x], []]  # close syns and hyponyms
                #only take verbs and nouns
                kwd_syns = wn.synsets(x)
                if not kwd_syns:
                    continue
                counter = 0
                words_temp_syns = []
                words_temp_hyps = []
                if x in self.final_word_dict.keys():
                    continue
                # TODO: add a separate loop for homonyms
                cached_kwd_syns = set(copy.deepcopy(kwd_syns))
                for i in kwd_syns:
                    #TODO(mrafi): remove negative kwds.
                    negative_keywords = self.get_negative_keywords(
                            neg_kwds, i)
                    cached_kwd_syns = cached_kwd_syns - set(negative_keywords)
                    if not cached_kwd_syns.__contains__(i):
                        continue
                    if not self.config.get('include_all_pos_types') and i.pos not in ('n', 'v', 'a'):
                        continue
                    if self.config['close_syns']:
                        types_of_kwd = i.lemmas  # XXX:for synonyms this is it
                        temp = sorted(i.lemma_names)
                        #if i in
                        for j in temp:
                            words_temp_syns.append('%s ' % (j.replace('_', ' ')))
                    if self.config['hypo_syns']:
                        types_of_kwd = i.hyponyms()  # data for hyponyms
                        temp = sorted([lemma.name for synset in types_of_kwd for lemma in synset.lemmas])
                        for j in temp:
                            words_temp_hyps.append('%s ' % (j.replace('_', ' ')))
                    if not types_of_kwd:
                        continue
                    counter += 1
                if words_temp_syns:
                    synsxx[kwd][x][0] = sorted(list(set(words_temp_syns)))
                if words_temp_hyps:
                    synsxx[kwd][x][1] = sorted(list(set(words_temp_hyps)))
        return synsxx

    def permute_wrapper(self, raw_dict):
        """Iteratively permutes over the key value pairs of raw_dict

        Args:
            raw_dict: a dictionary containing word as key
                 and a dictionary as values
                 Something like this:
                 >>> {'foo bar': {'foo': ['z', 'n', 'o'], 'bar': ['x', 'y', 'm']},
                      'rafi': {'rafi': ['a', 'b', 'c', 'd']}}

        Returns:
            a dictionary of permuted words as values.
            eg:
            >>> {'foo bar': ['z x', 'z y', 'z m', 'n x', 'n y', 'n m', 'o x', 'o y', 'o m'],
                 'rafi': ['a', 'b', 'c', 'd']}"""

        for keyword, word_dict in raw_dict.items():
            self.permuterex(word_dict.values(), '', 0)
            self.final_word_dict[keyword] = self.kwd_list
            self.kwd_list = []
            self.word_dict = {}
        return self.final_word_dict

    @classmethod
    def thes_kwdgen(cls, kwd_dict):
        #kwd_dict is a dict with keywords as a key and value as a dict with words as key and list of syns and hyps as values
        # kwd_dict = {kwd1:{word1:[syns+hyps], ..}..}
        words = []
        #returned dict
        final_kwd_dict = {}
        for kwd in kwd_dict:
            final_kwd_dict[kwd] = []
            for wrd in kwd_dict[kwd]:
                words.append(list(kwd_dict[kwd][wrd]))
            cls.permuterex(words, '', 0)
            final_kwd_dict[kwd] = cls.kwd_list
        return final_kwd_dict

    def flatten_synonyms_dict(self, synonyms_dict):
        for i, j in synonyms_dict.items():
            for m, n in j.items():
                synonyms_dict[i][m] = [item for sublist in n for item in sublist]
        return synonyms_dict


def main(source_keywords, negative_keywords=[],
         close_syns=True, hypo_syns=True,
         include_all_pos_types=True):
    config_dict = dict(close_syns=close_syns, hypo_syns=hypo_syns,
         include_all_pos_types=include_all_pos_types)
    thesaurus_obj = MainThesaurusHandler(source_keywords, config_dict)
    synonyms_dict = thesaurus_obj.generate_thesaurus(negative_keywords)
    synonyms_dict = thesaurus_obj.flatten_synonyms_dict(synonyms_dict)
    final_synonym_dict = thesaurus_obj.permute_wrapper(synonyms_dict)
    print 'Original Word, **Synonymns List'
    for src_word, synonyms in final_synonym_dict.items():
        print src_word, ',', ', '.join(synonyms)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Thesaurus words for a set source of words. \n'
        'Example Usage: python core/thes_wordnet.py iron_man -n human -n officer --exclude-hyponyms\n'
        'This would get all synonyms of iron man and permute over it. It will also exclude the human and officer context.')
    parser.add_argument('source_keywords', metavar='w',
                        type=str, nargs='+',
                        help='Source set of keywords, for which you want to get synonyms. add underscore(_) for multiple joined words ex: motor_car, bat_man')
    parser.add_argument('-n', dest='negative_keywords',
                        action='append', type=str, default=[],
                        help='Negative keywords.')
    parser.add_argument('--exclude-synonyms', dest='synonyms',
                        action='store_const', const=False, default=True,
                        help='')
    parser.add_argument('--exclude-hyponyms', dest='hyponyms',
                        action='store_const', const=False, default=True,
                        help='')

    args = parser.parse_args()
    # Clean up the user input keywords.
    source_keywords = [' '.join(i.split('_')) for i in args.source_keywords]
    negative_keywords = [' '.join(i.split('_')) for i in args.negative_keywords]
    main(source_keywords, negative_keywords=negative_keywords,
         close_syns=args.synonyms, hypo_syns=args.hyponyms)
