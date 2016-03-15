from flask import Flask, render_template, request, redirect, url_for, Response
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

import ChooseWord as cw
import CustomNames as cn
import PrepareWords as pw

app = Flask(__name__)

@app.route('/')
def index():
    
    describe_projects = cw.create_thesaurus_name()

    return render_template('tabbedindex.html',
                           describe_projects = describe_projects)

@app.route('/custom-words/<string:user_word>')
def CustomName(user_word):

    word_list = user_word.split('-')
    project_names = cn.custom_names(word_list)
    
    return render_template('customnames3.html',
                           project_names = project_names,
                           user_word = user_word)

@app.route('/custom-words', methods=['GET'])
def CustomWords():
    
    user_word = request.args['words']
    
    word_list = pw.clean_words(user_word)
    #if not word_list:
        #return redirect(url_for('index'))
        
    redirect_string = pw.create_redirect_string(word_list)
	
    return redirect (redirect_string)

@app.route('/sentiment', methods=['GET'])
def Sentiment():

    return render_template ('sentiment.html')

@app.route('/sentiment-analysis', methods=['POST'])
def SentimentAnalysis():

    user_word = request.form['words']
    word_list = user_word.split()
    count = CountVectorizer()
    docs = np.array([user_word])
    bag = count.fit_transform(docs)
    word_map = count.vocabulary_
    bag_array = bag.toarray()

    tfidf = TfidfTransformer()
    np.set_printoptions(precision=2)
    tfidf_array = tfidf.fit_transform(count.fit_transform(docs)).toarray()

    return render_template ('sentiment-analysis.html', word_list=word_list,
    			    word_map=word_map, bag_array = bag_array, tfidf_array=tfidf_array)
    

@app.route('/sitemap.xml', methods=['GET'])
def SiteMap():
    xml = render_template('sitemap.xml')
    return Response(xml, mimetype='text/xml')
	
if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=33507)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
