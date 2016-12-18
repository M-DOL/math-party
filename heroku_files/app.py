from flask import Flask, render_template, jsonify
#import extensions
import controllers

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the controllers
app.register_blueprint(controllers.student)
app.register_blueprint(controllers.teacher)

# Register the api controller
app.register_blueprint(controllers.api_class, url_prefix='/api')
app.register_blueprint(controllers.api_new_student, url_prefix='/api')

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(debug=True)
