import os
import openai
from gtts import gTTS
from googletrans import Translator
from flask import Flask, request, render_template, make_response
from flask_cors import CORS


app = Flask(__name__, template_folder='.', static_folder='static')
app.debug = True
CORS(app)

tr = Translator()
openai.api_key = "" # tsy atao banga


def transform(text):
	text = text.replace('dr', 'j')
	text = text.replace('ts', 'tch')
	text = text.replace('tr', 'tch')
	text = text.replace('y', 'i')
	text = text.replace('s', 'ss')
	text = text.replace('e', 'é')
	text = text.replace('?', '')
	return text


def read_text(text):
	try:
		tts = gTTS(text=text, lang='fr', slow=False)
		tts.save("static/out.mp3")
		return True
	except:
		return False


def to_fr(text):
	return tr.translate(text, dest="fr").text


def to_mg(text):
	return tr.translate(text, dest="mg").text


def answer(prompt):
	try:
		disc = [{
	        'role': 'user',
	        'content': prompt
        }]
		ans = openai.ChatCompletion.create(
			model="gpt-3.5-turbo-1106",
			max_tokens=1024,
			n=1,
			stop=None,
			temperature=0.7,
			user="Mahay",
			messages=disc
		)
		return ans['choices'][0]['message']['content']
	except openai.error.OpenAIError as e:
		print(e)
		return None


@app.route('/', methods=['GET'])
def web():
	"""
	Mamoka interface web
	Ilay interface web tokony misy player mi-pointe out.mp3
	"""
	return render_template('index.html')


@app.route('/read', methods=['POST'])
def read():
	"""
	Parametre "prompt" dia ilaina:
	POST http://localhost:99/read?prompt=fanontaniana_teny_gasy
	"""
	if 'prompt' in request.args:
		prompt = request.args.get('prompt')
		fr_prompt = to_fr(prompt)
		response = answer(fr_prompt)
		if response:
			mg_response = to_mg(response)
			success = read_text(response)
			if success:
				# commenter-o ito raha tsy atao play auto
				# os.system("start out.mp3")
				return make_response({
					'status': 200,
					'message': mg_response
				}, 200)
			else:
				return make_response({
					'status': 500,
					'message': "Error"
				}, 500)
		else:
			return make_response({
				'status': 500,
				'message': "Error"
			}, 500)
	else:
		return make_response({
			'status': 400,
			'message': "Missing 'prompt' argument"
	}, 400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)