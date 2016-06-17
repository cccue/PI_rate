import io_funcs
import numpy as np

full_data = io_funcs.get_data_from_objects()

# Computing histograms and related data for all reviews
def build_all_reviews_hist(full_rum_data,tag_label):
    
    if (tag_label == "user rating"):
       min_range = 1
       max_range = 10
    elif (tag_label == "sentiment"):
       min_range = 0.
       max_range = 1.0   
    
    data_for_hist = []
    mean_list = []
    for index_rum in range(0,len(full_rum_data)):
        data_loc = full_rum_data[index_rum]["data"][tag_label]
        for index_rev in range(0,len(data_loc)):
            data_for_hist.append(data_loc[index_rev])
        mean_list.append(data_loc.mean())
    
    #print "Total reviews: ", len(data_for_hist)
    mean_full = np.sum(data_for_hist).astype('float')/len(data_for_hist)
    full_hist, bin_edges = \
    np.histogram(data_for_hist,bins=10,range=(min_range,max_range),density=True)
    
    return full_hist, mean_list, mean_full

# Creating the Json structure to feed the d3 force-directed graph generator
def create_data_for_graph(data,mean_list):

    nodes_list = []
    links_list  = []
    nodes_list.append({"name":"Generic user","group":0,"value":"./static/images/user.png","page":""})
    
    for index in range(0,len(data)):
        
        nodes_list.append({"name":data[index]["rum name"] +", id: " + \
        str(index) + ", rating: " + \
        str("%.2f" % mean_list[index]),"group":int(round(mean_list[index])),\
        "value":"./static/images/ron_bottle.png","page":"https://www.rumratings.com"})
        links_list.append({"source":index+1,\
        "target":0,"value":2*mean_list[index]})
        
    dic_for_Json = {"nodes":nodes_list,"links":links_list}

    return dic_for_Json

# Creating the Json structure to feed the table generator
def create_data_for_table(brand_list,ratings_list,counts_list): 

    nodes_list = []

    for index in range(0,len(brand_list)):
        nodes_list.append({"name":brand_list[index],\
        "rating":ratings_list[index],"users":counts_list[index]})

    dic_for_Json = {"nodes":nodes_list}

    return dic_for_Json
