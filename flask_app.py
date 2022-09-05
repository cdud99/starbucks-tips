#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, send_file
import git, hmac, hashlib, os, sys, io, eNotify, traceback, secrets

from PDFReader import scanPDF
from PDFWriter import writePDF

from FileManager import main as checkFiles

from partnerInfoGetter import get_sq

# Send standard output to variable to send by email later
oldstdOut = sys.stdout
starbucksTipsOutput = io.StringIO()
sys.stdout = starbucksTipsOutput

app = Flask(__name__)

# Set absolute path to processed tips folder
processedReportsPath = '/home/cdud99/webupdater/static/ProcessedTips'
# processedReportsPath = 'static/ProcessedTips'

# Get secret key to verify with GitHub
w_secret = os.getenv('SECRET_KEY')




# Function to return simple errror message to users browser
def pageError():
    return '''
        <html>
            <body>
                <p>Oh No!</p>
                <p>Looks like there was a problem</p>
                <p>The developer has been notified of the issue you experienced, please feel free to try that again and if the problem persists check back in the next few days</p
            </body>
        </html>
    '''



@app.route('/')
def index():

    # Set up try/except block in case of error
    try:

        amount = ''
        invalidPDF = ''

        if request.args.get('amount') != None:
            amount = request.args['amount']
        if request.args.get('invalidPDF') != None:
            invalidPDF = request.args['invalidPDF']

        # Run script to check whether files have expired and delete them
        checkFiles(processedReportsPath)

        # Let flask render index.html file
        return render_template('index.html', amount = amount, invalidPDF = invalidPDF)

    # Catch exception in variable "e"
    except Exception as e:

        # On exception print exception data to stdout which is in a variable now
        print(type(e), e, traceback.format_exc())

        # Send subject and stdout to eNotify to email developer about error
        eNotify.notify('Starbucks Tips Error', starbucksTipsOutput.getvalue())

        # Return error message for user
        return pageError()



@app.route('/process-report', methods=['POST', 'GET'])
def process_report():

    # Set up try/except block in case of error
    try:

        # Only run code here if this route recieves a POST request
        if request.method == 'POST':

            # Get tip amount from the first field of the form
            amount = int(request.form['tip-amount'])

            # Get the tip report file submitted by user
            file = request.files['file']

            # Generate random hex name for pdf to differentiate between multiple users
            # and create file path from the generated token
            fileName = secrets.token_hex(10) + '.pdf'
            filePath = os.path.join(processedReportsPath, fileName)

            # Extract text from Starbucks tip report and organize into dict
            pdf = scanPDF(file, amount)

            # If scanPDF returns None it means the pdf submitted was invalid
            if pdf == None:
                return redirect('/?amount={}&invalidPDF={}'.format(amount, 'true'))

            # Write the new tip report using the dict
            writePDF(pdf, filePath)

            # Send current users file as an attachment with a preset name
            return send_file(filePath, as_attachment=True, attachment_filename='CalculatedTips.pdf')

        # If user happens to enter this route redirect them to the main page
        return redirect('/')

    # Catch exception
    except Exception as e:

        # On exception print exception data to stdout which is in a variable now
        print(type(e), e, traceback.format_exc())

        # Send subject and stdout to eNotify to email developer about error
        eNotify.notify('Starbucks Tips Error', starbucksTipsOutput.getvalue())

        # Return error message for user
        return pageError()



# Function to check validity of GitHub signiture on signal to pull repository
def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

# Route only for updating another app
@app.route('/update_server', methods=['POST'])
def webhook():

    # Check for POST data
    if request.method == 'POST':

        try:

            # Get GitHub signature data
            x_hub_signature = request.headers.get('X-Hub-Signature')

            # Check for signature validity and return code 400 if invalid
            if not is_valid_signature(x_hub_signature, request.data, w_secret):
                return 'Invalid Signature', 400

            # Set directory of git repository and select remote origin
            repo = git.Repo('./mysite')
            origin = repo.remotes.origin

            # Pull any data from repository and merge
            origin.pull('main')

            # If there are no errors print to stdout variable and send confirmation email
            print('Updated successfully')
            eNotify.notify('Starbucks Tips Updater', starbucksTipsOutput.getvalue())

            # Return code 200 for GitHub verification
            return 'Updated PythonAnywhere successfully', 200

        except Exception as e:

            # On exception print exception data to stdout which is in a variable now
            print(type(e), e, traceback.format_exc())

            # Send subject and stdout to eNotify to email developer about error
            eNotify.notify('Starbucks Tips Updater Error', starbucksTipsOutput.getvalue())

            # Return error message for GitHub with code 400
            return 'Error: ' + starbucksTipsOutput.getvalue(), 400

    # If POST data does not exist return code 400
    else:
        return 'Wrong input type', 400

@app.route('/getSQ', methods=['GET'])
def get_security_questions():
    if request.method == 'GET':
        numbers = request.headers.get('numbers')

        questions = get_sq(numbers)

        return {
        'question_one': questions[0],
        'question_two': questions[1],
        }

# For local testing only
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

