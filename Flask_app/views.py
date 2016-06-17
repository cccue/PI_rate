from Flask_app import app
from flask import render_template, make_response
import json
import analyzer_nlp
import analyzer

@app.route("/")
@app.route("/index.html")
@app.route("/index")
def front_page():
    
    """ Render front page template """
    return render_template('index.html', title="PI-rate")

@app.route("/word_cloud")
def cloud_page():

    return render_template('word_cloud.html', title="PI-rate")

@app.route('/make_cloud/<rum_id>', methods=['GET'])
def make_cloud(rum_id):

    key_value_common_pairs = analyzer_nlp.make_cloud(int(rum_id))

    return make_response(json.dumps(key_value_common_pairs))

@app.route("/rum_universe")
def rum_universe():

    return render_template('rum_universe.html', title="PI-rate")

@app.route("/rum_similarity")
def rum_sim():

    return render_template('rum_similarity.html', title="PI-rate")

@app.route("/about")
def about():

    return render_template('about.html', title="PI-rate")

@app.route("/histograms")
def plot_histograms():

    return render_template('histograms.html', title="PI-rate")

@app.route("/rum_name_list")
def rum_names():

    return render_template('rum_list.html', title="PI-rate")

@app.route("/make_hists/<rum_id>", methods=['GET'])
def make_histograms(rum_id):

    json_obj = analyzer.make_hists(int(rum_id))

    return make_response(json.dumps(json_obj))

@app.route("/make_graph", methods=['GET'])
def make_graph():
    
    json_obj = analyzer_nlp.make_graph()     

    return make_response(json.dumps(json_obj))

@app.route("/make_sim_table/<rum_id>", methods=['GET'])
def make_sim_table(rum_id):

    json_obj = analyzer.make_sim_table(int(rum_id))
 
    return make_response(json.dumps(json_obj))

@app.route("/make_rum_list")
def make_rum_list():

    json_obj = analyzer.make_rum_list()

    return make_response(json.dumps(json_obj))    
