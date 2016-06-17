#!/usr/bin/python
import pandas as pd
import subprocess
import numpy as np
import initialization

# Data for histograming within D3
def data_4_hist(data,tag_label):
  
    data_for_hist = []
    for index_rum in range(0,len(data)):
        data_loc = data[index_rum]["data"][tag_label]
        for index_rev in range(0,len(data_loc)):
            data_for_hist.append(data_loc[index_rev])
        
    return data_for_hist 

# Constructing the data from the user perspective 
def build_stats(data,tag = "user rating"):
 
    user_list = []
    rum_name_list = []
    data_list = []
    for index in range(0,len(data)):
        rum_name = data[index]["rum name"]
        rum_name_list.append(rum_name)
        users = data[index]["data"]["user name"]
        for uindex in range(0,len(users)):
            if users[uindex] in user_list:
               #print "user already in list:", users[uindex], rum_name
               index_list = user_list.index(users[uindex])
               #print "index list:", index_list
               data_list[index_list][rum_name] = \
               data[index]["data"][tag][uindex]
            else:
               user_list.append(users[uindex])
               dic = {"user name":users[uindex], \
                      rum_name:data[index]["data"][tag][uindex]}
               data_list.append(dic)
            
    return user_list, rum_name_list, data_list

# Building pair-correlation matrix  
def matrices_for_viz(userlist, rumlist, datlist):
   
    # Number of rum brands and registered users
    N_rums = len(rumlist)
    N_users = len(datlist)
    
    # Matrix initialization
    sim_mat = np.zeros((N_rums,N_rums))
    counter_mat = np.zeros((N_rums,N_rums)).astype('int')
    
    # Looping over all registered users
    for user_index in range(0,N_users):

        # Local list of rums and user names 
        loc_list = datlist[user_index].keys()
        # Looping over list of rum pairs
        for j_index in range(0,len(loc_list)):
            first_brand = loc_list[j_index]
            for i_index in range(j_index,len(loc_list)):
                second_brand = loc_list[i_index]
                # Skipping user info from list
                if ((first_brand != "user name") and \
                   (second_brand != "user name")):
                
                    first_index = rumlist.index(first_brand)
                    second_index = rumlist.index(second_brand)
                    # Computing ratings differences
                    delta = \
                    (float((datlist[user_index][first_brand])) - \
                    float((datlist[user_index][second_brand])))
                    # Invert sign if first rum index larger than
                    # second one. This ensure differences are always
                    # computed the same way
                    if (first_index > second_index):
                        delta *= -1
                    
                    sim_mat[first_index][second_index] += delta
                    counter_mat[first_index][second_index] += 1
                    
                    # Symmetrizing matrices
                    sim_mat[second_index][first_index] = \
                    sim_mat[first_index][second_index]
                    
                    counter_mat[second_index][first_index] = \
                    counter_mat[first_index][second_index]
        
    return sim_mat, counter_mat

# Building list of equally-liked rum brands for a given input 
def equally_liked_list(rum_name,rumlist,sim_matrix,counter_matrix):
    
    sorted_brands = []
    sorted_ratings_diff = []
    sorted_user_counts = []

    # Find rum name position in list
    rum_index = rumlist.index(rum_name)
    
    # Sorting indices to generate list of equally liked rums
    # based on absolute vale
    index_list = np.argsort(np.abs(sim_matrix[rum_index]))
    
    # Negative similarity numbers indicate less good brands
    # while positive numbers refer to better barnds
    for index in range(0,len(index_list)):
        r_index = index_list[index]
        if (rumlist[r_index] != rum_name):
           signo = -1.0
           if (rum_index > r_index): signo = 1.0
           # Only add cases with at least one reviewer
           if (counter_matrix[rum_index][r_index]) > 0:
              sorted_brands.append(rumlist[r_index])     
              sorted_ratings_diff.append(signo*sim_matrix[rum_index][r_index])  
              sorted_user_counts.append(counter_matrix[rum_index][r_index])

    return sorted_brands, sorted_ratings_diff, sorted_user_counts    

# Composing data table dictionary for Json object
def make_sim_table(rum_id):

    print "Rum id is ", rum_id
    data = initialization.full_data
    if( 0<= rum_id < len(data) ):
      print "Rum name is ", data[rum_id]["rum name"]
      userlist, rumlist, datlist = build_stats(data,"user rating")
      sim_mat, counter_mat = matrices_for_viz(userlist, rumlist, datlist)
      sim_mat_norm = np.divide(sim_mat,counter_mat)
      brand_list, ratings_list, counts_list = \
      equally_liked_list(data[rum_id]["rum name"], \
      rumlist,sim_mat_norm,counter_mat) 

      dic_for_Json = \
      initialization.create_data_for_table(brand_list,ratings_list,counts_list)
    else:
      dic_for_Json = {"nodes":[{"name":"Invalid index entry. See reference table for list of rum indices associated to each avaliable rum bottle.","rating":"N/A",\
      "users":"N/A"}]}

    return dic_for_Json

# Composing data histogram dictionary for Json object
def make_hists(rum_id):

    data = initialization.full_data

    if(-1<= rum_id < len(data)):
      if (rum_id == -1):
         hist_rating = data_4_hist(data,"user rating")
         hist_sentiment = data_4_hist(data,"sentiment")
      else:
         hist_rating = data[rum_id]["data"]["user rating"]
         hist_sentiment = data[rum_id]["data"]["sentiment"]

      full_hist_rating = data_4_hist(data,"user rating")
      full_hist_sentiment = data_4_hist(data,"sentiment")

      dic_for_Json = \
      {"rating":[{"local":list(hist_rating),"full":list(full_hist_rating)}],\
      "sentiment":[{"local":list(hist_sentiment),"full":list(full_hist_sentiment)}]}

    return dic_for_Json

# Composing list of available rum names
def make_rum_list():

    data = initialization.full_data

    rum_name_list = []

    for index in range(0,len(data)):
        rum_name_list.append(data[index]["rum name"])

    dic_for_Json = {"rum_names":rum_name_list}
    return dic_for_Json
