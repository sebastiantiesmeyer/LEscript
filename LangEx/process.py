from flask import Flask, request, jsonify
import os
# from config import Config

app = Flask(__name__)
# app.config.from_object(Config)

@app.route('/api', methods = ['POST'])
def api():
    # print('chill!')
    # Do something useful here...

    inp = request.values.get('input', '')

    if len(inp)<200:

        with open('data.txt','w') as file:

            file.write(inp)

        print(inp)

        return ("Thanks for inscribing! \
                You'll receive a confirmation \
                mail before the beginning of the event.")

    # else:
    #     return("Your input is too long, unfortunately... Please select fewer languages.")

# print('chill!1')
  
