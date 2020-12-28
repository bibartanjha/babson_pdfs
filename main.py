from flask import Flask, render_template, url_for, request, redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import re 
import pymongo
from pymongo import MongoClient

mail_content = 'Test mail'

sender_address = 'babsonpdfgenerator@gmail.com'
sender_pass = '2o3rok3efk'
receiver_address = 'bibartanjha@gmail.com'

client = pymongo.MongoClient("mongodb+srv://babson_pdfs:S4GhKHWkWWUzNzCy@cluster0.up2il.mongodb.net/Jobs?retryWrites=true&w=majority")

app = Flask(__name__)

@app.route('/')
def main_func():
	return render_template('index.html')

@app.route('/Create_Document', methods=['GET', 'POST'])
def CreateDocument():
	return render_template('create_document.html')

@app.route('/Documents', methods=['GET', 'POST'])
def Documents():
	return render_template('documents.html')

@app.route('/Create_Job', methods=['GET', 'POST'])
def CreateJob():
	if request.method == 'POST':
		db = client['Jobs']
		collection = db['Jobs']

		true_emails = re.findall('[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}', request.form['recipients'])
		if len(true_emails) == 0:
			return render_template('create_job.html', job_created = True, job_successful = False)
		
		job_info = {}
		job_info['Job Name'] = request.form['jobName']
		job_info['Job Description'] = request.form['jobDescription']
		job_info['Email Subject'] = request.form['emailSubject']
		job_info['Email Body'] = request.form['emailBody']
		job_info['Recipients'] = true_emails

		record_submitted = collection.insert_one(job_info)
		return render_template('create_job.html', job_created = True, job_successful = True, job_info = job_info)
	return render_template('create_job.html', job_created = False)

@app.route('/Jobs', methods=['GET', 'POST'])
def Jobs():
	db = client['Jobs']
	collection = db['Jobs']
	all_jobs = []
	for doc in collection.find():
		all_jobs.append(doc)
	return render_template('jobs.html', all_jobs=all_jobs)

@app.route('/Send_PDFs', methods=['GET', 'POST'])
def Send_PDFs():
	return render_template('send_pdfs.html')

@app.route('/Output_History', methods=['GET', 'POST'])
def Output_History():
	return render_template('output_history.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


