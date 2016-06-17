import subprocess
from sklearn.externals import joblib

# Gathering reviewed data from storage folder/objects
def get_data_from_objects():

    root_folder = 'Flask_app/static/objects/data/'
    command = 'ls ' + root_folder
    # To list all files with rum reviews
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, \
                         stderr=subprocess.STDOUT)

    # Building list of dictionaries with full set of review data
    full_rum_data = []
    for line in p.stdout.readlines():
        rum_object = line.strip('\n')
        file_name = root_folder + rum_object
        data = joblib.load(file_name)
        full_rum_data.append(data)

    return full_rum_data

