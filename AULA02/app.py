from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os, json
import getpass
from os import listdir
from os.path import isfile, join
import requests, bs4   # pip install beautifulsoup4 requests

mypath = "/home/flaskman/Documentos/curso_flask_puc/AULA02/downloads"
#username = getpass.getuser()
username = "walter"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def uploadFiles():
	if request.method == 'POST':
		if 'file' not in request.files:
			return render_template('upload_files.html', username=username)

		files = request.files.getlist('file')
		
		for file in files:
			filename = secure_filename(file.filename)
			file.save(os.path.join(mypath, filename))

		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		return render_template('relatorio.html', onlyfiles=onlyfiles, username=username)

	return render_template('upload_files.html', username=username)

@app.route('/download', methods=['GET', 'POST'])
def downloadFile():
	if request.method == 'POST':
		filename = request.form['filename']
		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		
		if 'filename' not in request.form:
			return render_template('upload_files.html', username=username, onlyfiles=onlyfiles)

		path = 'downloads/' + filename
		return send_file(path, as_attachment=True)
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	return render_template('download_file.html', username=username, onlyfiles=onlyfiles)

@app.route('/weather', methods=['GET', 'POST'])
def climaTempo():
	if request.method == 'GET':
		url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/182/pocosdecaldas-mg'
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.text, 'html.parser')

		temp_min = soup.find(id = 'min-temp-1')
		print("temp min: " + temp_min.contents[0])
		temp_min = str(temp_min.contents[0])

		json_object = json.loads('{ "primeiro_dado":"%s"}' % temp_min)
		json_formatted = json.dumps(json_object, indent=2)
		print(json_formatted)
		return jsonify({"return": json_formatted}), 200
	return jsonify({"return"})

if __name__ == "__main__":
	app.run()
