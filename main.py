from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'
#
#
# @app.route('/about')
# def about():
#         return 'This is the about page.'
#
#
# @app.route('/user/<username>')
# def show_user_profile(username):
#         return f'User {username}'
#
#
# @app.route('/user/<int:user_id>')
# def show_user_profile_by_id(user_id):
#         return f'User with id {user_id}'
#
#
# @app.route('/files/<path:filepath>')
# def show_file(filepath):
#         return f'File located at: {filepath}'

if __name__ == '__main__':
    app.run(debug=True)