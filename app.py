# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from consumer import consumer
#from flask import Flask

#app = Flask(__name__)

#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


# if __name__ == '__main__':
    # app.run()

if __name__ == '__main__':
    consume = consumer()
    consume.recive('exception')