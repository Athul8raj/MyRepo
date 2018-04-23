from flask import Flask,render_template, request
import requests, time
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import urllib
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')
	
@app.route('/IsItPlagiarized/', methods=['POST'])
def IsItPlagiarized():
	text_to_filter=request.form['text_to_check']
	if (text_to_filter.lstrip().rstrip() == ''):
			return render_template('index.html')
	punkt_param = PunktParameters()
	sentence_splitter = PunktSentenceTokenizer(punkt_param)
	sentences = sentence_splitter.tokenize(text_to_filter)
	probability_of_plagiarism = 0
	for a_sentence in sentences:
			time.sleep(0.3)
			content = str(filter(lambda x: x in string.printable, a_sentence))
			the_term = urllib.parse.quote('+' + '"' + content + '"')
			page = requests.get('https://www.bing.com/search?q='+the_term)
			if (not "No results found for" in page.text):
					probability_of_plagiarism += 1;
	is_it_plagiarized = str((probability_of_plagiarism / len(sentences)) * 100) + '%'
	return render_template('result.html', text_to_filter=text_to_filter, is_it_plagiarized=is_it_plagiarized)	
	
if __name__ == '__main__':
	app.run(debug=True)