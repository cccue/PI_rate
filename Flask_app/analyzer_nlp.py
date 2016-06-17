import nltk
import string
import os
import re
from collections import Counter
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import analyzer
import json
from sklearn.externals import joblib
import initialization

# Concatenating all titles and review texts for English reviews
# into single string for a given brand
def build_text_for_brand_cloud(data):
    ecounter = 0
    for rindex in range(0,len(data["data"]["language"])):
        language = data["data"]["language"][rindex].strip()
        if(language == "English"):
          ecounter += 1
          if(ecounter == 1):
            brand_text = data["data"]["user review title"][rindex] + \
                        data["data"]["user review"][rindex]
          else:
            brand_text += data["data"]["user review title"][rindex] + \
                        data["data"]["user review"][rindex]
                
    return brand_text    
      
# Concatenating all titles and review texts for English reviews
# into single string for all brands
def build_text_for_site_cloud(data):
    for brand_index in range(0,len(data)):
        data_brand = data[brand_index]
        brand_text = build_text_for_brand_cloud(data_brand)   
        if(brand_index == 0): 
          full_text = brand_text
        else:
          full_text += brand_text
        
    return full_text 

# To tokenize a string of text
def get_tokens(text):
    # Lowercasing
    lowers = text.lower()
    # Removing punctuation
    no_punctuation = re.sub(ur'[^\w\s]','',lowers)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens

# Getting list of tuples with most first most common 
# N_terms words
def most_common_terms(text,N_terms):

    tokens = get_tokens(text)
    bi_tokens = nltk.bigrams(tokens)
    tri_tokens = nltk.trigrams(tokens)

    Stopwords = stopwords.words('english')
    # Adding my list of extra stop words that I consider do not add
    # meaning to understand the reviews
    extra_list = ['is a','on the','in the','it is','this is','would',\
                 'this one','of the','of this','one','its a','for a',\
                 'a bit','one of','for the','get','in a','it was','to be',\
                 'it has','with a','as a','use','use for','used','used for',\
                 'to the','one is','of my','one of the','one of my','and a',
                 'really']
    Stopwords.extend(extra_list)

    tokens = \
    [token for token in tokens if token not in Stopwords]
    bi_tokens = [' '.join(token) for token in bi_tokens]
    bi_tokens = \
    [token for token in bi_tokens if token not in Stopwords]
    tri_tokens = [' '.join(token) for token in tri_tokens]
    tri_tokens = \
    [token for token in tri_tokens if token not in Stopwords]

    common_tokens = []
    common_tokens.extend(tokens)
    common_tokens.extend(bi_tokens)
    common_tokens.extend(tri_tokens)
    count = Counter(common_tokens)

    return count.most_common(N_terms)

# Creating Json object for the javascript cloud maker
def prepare_for_Json(common_words):
  
    key_value_common_pairs = []
    for index in range(0,len(common_words)):
       dic = {"key":str(common_words[index][0]), \
              "value":int(common_words[index][1])}
       key_value_common_pairs.append(dic)

    return key_value_common_pairs

# Getting data for cloud algorithm
def make_cloud(rum_id):

    #print (os.getcwd() + "\n")
    object_root_folder = 'Flask_app/static/objects/clouds/'
    cloud_file_name = \
    object_root_folder + 'word_cloud_' + str(rum_id) + '.pkl'
    
    if(os.path.exists(cloud_file_name)):
       key_value_common_pairs = joblib.load(cloud_file_name)
    else:

       N_terms = 40
       print "Building word cloud object"
       #data = analyzer.get_data_from_objects()
       data = initialization.full_data
       if( -1<= rum_id < len(data)):
         # Index -1 builds the common words list for the full site
         if(rum_id == -1):
           full_text = build_text_for_site_cloud(data)
         # Builds the common words list for a given brand 
         else:
           full_text = build_text_for_brand_cloud(data[rum_id])
         common_words = most_common_terms(full_text,N_terms)
         key_value_common_pairs = prepare_for_Json(common_words)
         joblib.dump(key_value_common_pairs,cloud_file_name,compress=1)
       else:
         key_value_common_pairs =  [{"key":"Invalid index","value":600},\
         {"key":"Try again","value":550},{"key":"Out of range","value":450},\
         {"key":"Valid range: -1 to 118","value":350},\
         {"key":"check rum table again","value":200}]
       print "done building object"

    return key_value_common_pairs

# Building Json object for graph building 
def make_graph():

    data = initialization.full_data
    hist_full, mean_list, mean_full = \
    initialization.build_all_reviews_hist(data,"user rating")
    dic_for_json = initialization.create_data_for_graph(data,mean_list)

    return dic_for_json
