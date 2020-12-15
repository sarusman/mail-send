from flask import Flask, render_template, request, session, redirect
import smtplib, unidecode
from datetime import timedelta

app=Flask(__name__)
app.secret_key="3208932"


@app.route('/')
def index():
	return render_template('index.html', msg=session['msg'] if session.get('msg') else "")


@app.route('/send.ppv4.http+3+$$/<mails>/<sbj>/<msg>' , methods=["POST", "GET"])
def sender(mails, sbj, msg):
	if mails=="":
		return "<h1>Impossible</h1>"
	else:
		t=send(mails, sbj, msg)
		if len(t)==0:
			return "<h1>Message envoyé </h1><br>"
		else:
			return "<h1>Erreur lors de l'envoie à <strong>"+t+"</strong></h1><br>"



def send(mails, sbj, msg):
	mails=mails.replace(" ", "")
	mails=mails.split(';')
	#if len(mails)>15:
	#	mails=mails[0:15]
	conex=smtplib.SMTP('smtp.gmail.com:587')
	conex.starttls()
	err_l=[]
	conex.login('paulavoine53@gmail.com', '*')
	message=('Subject: {}\n\n{}'.format(sbj+'\n', msg))
	for i in mails:
		if "@" not in i and "." not in i:
			err_l.append(i)
		else:
			try:
				conex.sendmail('paulavoine53@gmail.com', i ,unidecode.unidecode(message))
			except:
				err_l.append(i)	
	return " ".join(err_l)





if __name__=="__main__":
	app.run(debug=True)
