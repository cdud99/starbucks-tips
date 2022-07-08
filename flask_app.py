
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template, redirect, send_file
import hmac, hashlib, os, sys, io, eNotify, traceback, secrets
# import git
from PDFReader import scanPDF
from PDFWriter import writePDF

from ProcessedTips.FileManager import main as checkFiles

oldstdOut = sys.stdout
outputToSend = io.StringIO()
sys.stdout = sys.stderr

app = Flask(__name__)

def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

w_secret = os.getenv('SECRET_KEY')


@app.route('/')
def hello_world():
    checkFiles('ProcessedTips')

    return render_template('index.html')


@app.route('/process-report', methods=['POST', 'GET'])
def process_report():
    if request.method == 'POST':
        amount = request.form['tip-amount']
        print(amount, file=sys.stderr)

        file = request.files['file']

        key = secrets.token_hex(10)

        pdf = scanPDF(file, int(amount))
        writePDF(pdf, key)

        return send_file('ProcessedTips/{}.pdf'.format(key), as_attachment=True, attachment_filename='CalculatedTips.pdf')


    return redirect('/')


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            x_hub_signature = request.headers.get('X-Hub-Signature')
            if not is_valid_signature(x_hub_signature, request.data, w_secret):
                return 'Invalid Signature', 400

            repo = git.Repo('./mysite')
            origin = repo.remotes.origin

            origin.pull('main')

            print('Updated successfully')
            eNotify.notify(outputToSend.getvalue())

            return 'Updated PythonAnywhere successfully', 200
        except Exception as e:
            print(type(e), e, traceback.format_exc())
            eNotify.notify(outputToSend.getvalue())
            return 'Error: ' + outputToSend.getvalue(), 400

    else:
        return 'Wrong input type', 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)

