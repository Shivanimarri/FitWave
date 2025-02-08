from flask import Flask, render_template, request, redirect, url_for,session
from pymongo import MongoClient
from datetime import datetime ,timedelta
from bson import ObjectId
from flask import abort
from jinja2 import Environment
from bson.json_util import dumps
import math
import pymongo
import requests
import random

app=Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/fitwave'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.get_database('fitwave')

collection = db['exercise page']
collection1 = db['form details']
collection2 = db['signup']
collection3 = db['R']
collection4 = db['progress']

# general routers

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/video1')
def video1():
    return render_template('video1.html')

@app.route('/video2')
def video2():
    return render_template('video2.html')

@app.route('/video3')
def video3():
    return render_template('video3.html')

from flask import render_template

@app.route('/video')
def video():
    # Get the video URL from the query parameter
    video_url = request.args.get('url')
    url0=request.args.get('url0')
    print(url0)
    # Get the user's email from the session
    user_email = session.get('email')

    # If the user's email is available
    if user_email:
        # Find the user's progress document in MongoDB
        progress_cursor = collection4.find({'email': user_email}).sort('_id', -1)
        latest_progress_document = progress_cursor[0] 

        # If the latest progress document exists
        if latest_progress_document:
            # Increment the count of video completion
            updated_count = latest_progress_document.get('count', 0) + 1

            # Update the progress document in the database
            collection4.update_one(
                {'_id': latest_progress_document['_id']},
                {'$set': {'count': updated_count}}
            )

            # Render the video template with the provided video URL
            return render_template('video.html', video_url=video_url,url0=url0)
        else:
            # Return a message if the progress document is not found
            return 'Progress document not found for the user'
    else:
        # Return a message if the user's email is not found in the session
        return 'User email not found in session'



@app.route('/week')
def week():
    email = session.get('email')

    if email:
        user_cursor = collection1.find({'email': email})
        user_profiles = list(user_cursor)  # Convert cursor to a list of documents

        if user_profiles:
            duration = user_profiles[-1].get('duration', 'User')  # Default to 'User' if name is not found
            weight = user_profiles[-1].get('weight', '')  # Get the weight from the user document
            goal_weight = user_profiles[-1].get('goal_weight', '')  # Get the duration from the user document
            goal = user_profiles[-1].get('goal', '')  # Get the goal from the user document

            value = math.ceil((goal_weight) / (duration * 10))

            user1_cursor = collection4.find({'email': email})
            user1=list(user1_cursor)

            if user1:
                video = int(user1[-1].get('video',''))
                count = int(user1[-1].get('count',''))

                overall_progress = (count / video) * 100 if video > 0 else 0

                response = requests.get("https://api.api-ninjas.com/v1/quotes")
                if response.status_code == 200:
                    quotes = response.json()
                    random_quote = random.choice(quotes)
                    quote_text = random_quote['text']
                    quote_author = random_quote['author'].split(',')[0]
                else:
                    quote_text = 'I hated every minute of training, but I said, Donnot quit. Suffer now and live the rest of your life as a champion.'
                    quote_author = 'Muhammad Ali'

                if goal == 'keepFit':
                    if value == 1:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_fe',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                    elif value == 2:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_fm',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                    elif value == 3:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_fh',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                elif goal == 'loseWeight':
                    if value == 1:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_le',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                    elif value == 2:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_lm',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                    elif value == 3:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_lh',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                elif goal == 'getStronger':
                    if value == 1:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_se',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                    elif value == 2:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_sm',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                    elif value == 3:
                        return render_template('week.html', duration=duration, goal=goal, url='exercise_sh',
                                               overall_progress=overall_progress, quote_text=quote_text, quote_author=quote_author)
                else:
                    abort(400)  # Handle invalid goal

        else:
            return "User not found."
    else:
        return "Email not found in session."


# Route for rendering the exercise page for losing weight with light intensity
@app.route('/exercise_le')
def exercise_le():
    exercise_doc = collection3.find_one({"_id": ObjectId("662b666462d813531405d0d7")})

    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [  
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_le'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

# Route for rendering the exercise page for losing weight with moderate intensity
@app.route('/exercise_lm')
def exercise_lm():
    exercise_doc = collection3.find_one({"_id": ObjectId("6623e18319c2444e81626125")})

    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_lm'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

# Route for rendering the exercise page for losing weight with heavy intensity
@app.route('/exercise_lh')
def exercise_lh():
    exercise_doc = collection3.find_one({"_id": ObjectId("6623e4cd19c2444e81626126")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_lh'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

# Route for rendering the exercise page for keeping fit with heavy intensity
@app.route('/exercise_fh')
def exercise_fh():
    exercise_doc = collection3.find_one({"_id": ObjectId("6623ea4719c2444e81626128")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_fh'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

# Route for rendering the exercise page for keeping fit with moderate intensity
@app.route('/exercise_fm')
def exercise_fm():
    exercise_doc = collection3.find_one({"_id": ObjectId("6623ec5219c2444e81626129")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_fm'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

@app.route('/exercise_fe')
def exercise_fe():
    exercise_doc = collection3.find_one({"_id": ObjectId("662b208625e01480e661173d")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_fe'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

@app.route('/exercise_se')
def exercise_se():
    exercise_doc = collection3.find_one({"_id": ObjectId("662b1dcb25e01480e661173c")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_se'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

@app.route('/exercise_sm')
def exercise_sm():
    exercise_doc = collection3.find_one({"_id": ObjectId("662b1a7225e01480e661173a")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_sm'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

@app.route('/exercise_sh')
def exercise_sh():
    exercise_doc = collection3.find_one({"_id": ObjectId("662b1c9425e01480e661173b")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = [
        {"name": exercise_doc.get("name1"), "url": exercise_doc.get("url1")},
        {"name": exercise_doc.get("name2"), "url": exercise_doc.get("url2")},
        {"name": exercise_doc.get("name3"), "url": exercise_doc.get("url3")},
        {"name": exercise_doc.get("name4"), "url": exercise_doc.get("url4")},
        {"name": exercise_doc.get("name5"), "url": exercise_doc.get("url5")},
        {"name": exercise_doc.get("name6"), "url": exercise_doc.get("url6")},
        {"name": exercise_doc.get("name7"), "url": exercise_doc.get("url7")}
    ]
    name=exercise_doc.get('name')
    url0='exercise_sh'
    return render_template('exercise1.html', exercises=exercises,name=name,url0=url0)

@app.route('/home')
def home():
    # Retrieve the email from the session
    email = session.get('email')

# Assuming you have a function to retrieve user details from the database based on the email
    user_cursor = collection1.find({'email': email})
    user_profiles = list(user_cursor)  # Convert cursor to a list of documents

    if user_profiles:
        user_name = user_profiles[-1].get('name', 'User')  # Default to 'User' if name is not found
        weight = user_profiles[-1].get('weight', '')  # Get the weight from the user document
        duration = user_profiles[-1].get('duration', '')  # Get the duration from the user document
        goal = user_profiles[-1].get('goal', '')  # Get the goal from the user document

        
        if check_last_display(email):
            return redirect(url_for('form'))
        else:
            return render_template('home page.html', user_name=user_name, weight=weight, duration=duration, goal=goal)
    else:
        # Handle case where user is not found
        return "User not found"  # You can redirect or render an error page instead

@app.route('/profile')
def profile():
    # Retrieve the email from the session
    email = session.get('email')
    
    if email:
        # Query the database to get the user's profile(s) based on the email
        user_profiles_cursor = collection1.find({'email': email})
        
        # Convert the cursor to a list to ensure it's not being modified after execution
        user_profiles = list(user_profiles_cursor)
        
        if user_profiles:
            # Extract weight and submission dates from each user profile
            weight_data = []
            submission_dates = []
            for user_profile in user_profiles:
                weight_data.append(user_profile['weight'])
                # Convert submission time to a string representation
                submission_date_str = user_profile['submission_time'].strftime('%Y-%m-%d')
                submission_dates.append(submission_date_str)
            return render_template('profile.html', profile=user_profiles[-1], weight_data=weight_data, submission_dates=submission_dates)
        else:
            # Handle case where user's profile(s) are not found
            return 'User profile(s) not found.'
    else:
        # Handle case where user is not logged in
        return 'Please log in to view your profile.'
        




@app.route('/logout')
def logout():
    # Clear the session data (logout)
    session.clear()
    return redirect(url_for('landing'))  # Redirect to the landing page after logout

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username or email exists in the database
        user = collection2.find_one({'username': username})
        
        if user and user['password'] == password:
            # Successful login
            session['email'] = user['email']
            return redirect(url_for('home'))  # Redirect to the dashboard or any other page(home page)
        else:
            # Invalid credentials
            return 'Invalid username/email or password. Please try again.'
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if collection2.find_one({'$or': [{'username': username}, {'email': email}]}):
            return 'Username or email already exists. Please choose a different one.'
        
        user_data = {
            'username': username,
            'email': email,
            'password': password  
        }
        collection2.insert_one(user_data)
        
        session['email'] = email
        return redirect(url_for('form'))
    else:
        return render_template('signup.html')

def check_last_display(email):
    last_displayed_entry = collection1.find({'email': email}, {'submission_time': 1}).sort('submission_time', -1).limit(1)
    if last_displayed_entry:
        last_displayed_time = last_displayed_entry[0]['submission_time']
        if datetime.now() - last_displayed_time >= timedelta(days=7):
            return True
    return False

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Extract form data
        name = request.form['Name']
        email = request.form['email']
        height = float(request.form['height'])  # Convert to float
        weight = float(request.form['weight'])  # Convert to float
        age = int(request.form['age'])  # Convert to int
        gender = request.form['gender']
        goal = request.form['goal']
        goal_weight = float(request.form['goalWeight'])  # Convert to float
        duration = int(request.form['duration']) * 4  # Convert to int and multiplyp
        submission_time = datetime.now()
        
        # Create a document to insert into MongoDB
        user_data = {
            'name': name,
            'email': email,
            'height': height,
            'weight': weight,
            'age': age,
            'gender': gender,
            'goal': goal,
            'goal_weight': goal_weight,
            'duration': duration,
            'submission_time': submission_time
        }
        
        # Insert the document into MongoDB
        result = collection1.insert_one(user_data)

        existing_progress_document = collection4.find_one({
              'email': email,
              'goal_weight': goal_weight,
              'goal': goal,
              'duration': duration
        })

        if not existing_progress_document:
               progress_data = {
                   'email': email,
                   'count': 0,
                   'video': duration*7*7,
                   'goal':goal,
                   'goal_weight':goal_weight,
                   'duration':duration
               }

               # Insert the document into MongoDB for progress tracking
               result_progress = collection4.insert_one(progress_data)
        
        # Optionally, you can handle the result or redirect the user to another page
        return redirect(url_for('home'))
    else:
        return render_template('form.html')

# excercise routers 

# thigh workout
@app.route('/exercise-thigh-begineer')
def thigh_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("661954df77ded31d89930aa0")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Thigh Workout'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-thigh-intermediate')
def thigh_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("66196ba577ded31d89930aa4")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Thigh Workout'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-thigh-advanced')
def thigh_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("66196b4177ded31d89930aa3")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Thigh Workout'
    return render_template('exercise.html', exercises=exercises,name=name)





# toned arm
@app.route('/exercise-toned-begineer')
def toned_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("66196ea577ded31d89930ab0")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Toned Arm'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-toned-intermediate')
def toned_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("66196e8177ded31d89930aaf")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Toned Arm'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-toned-advanced')
def toned_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("66196e4677ded31d89930aae")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Toned Arm'
    return render_template('exercise.html', exercises=exercises,name=name)





# hand and wrist
@app.route('/exercise-hand-begineer')
def hand_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("66196ef577ded31d89930ab1")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Hands and Wrists'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-hand-intermediate')
def hand_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("66196f2577ded31d89930ab2")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Hands and Wrists'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-hand-advanced')
def hand_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("66196f4077ded31d89930ab3")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Hands and Wrists'
    return render_template('exercise.html', exercises=exercises,name=name)






# facial exercise
@app.route('/exercise-facial-begineer')
def facial_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("66196f8977ded31d89930ab4")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Facial Exercises'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-facial-intermediate')
def facial_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("66196fa077ded31d89930ab5")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Facial Exercises'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-facial-advanced')
def facial_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("66196fca77ded31d89930ab6")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Facial Exercises'
    return render_template('exercise.html', exercises=exercises,name=name)






# biceps
@app.route('/exercise-biceps-begineer')
def biceps_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("6619702e77ded31d89930ab7")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Biceps'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-biceps-intermediate')
def biceps_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619704377ded31d89930ab8")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Biceps'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-biceps-advanced')
def biceps_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("6619706f77ded31d89930ab9")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Biceps'
    return render_template('exercise.html', exercises=exercises,name=name)






# triceps 
@app.route('/exercise-triceps-begineer')
def triceps_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("661970ac77ded31d89930aba")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Triceps'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-triceps-intermediate')
def triceps_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("661970c077ded31d89930abb")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Triceps'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-triceps-advanced')
def triceps_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("661970f477ded31d89930abc")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Triceps'
    return render_template('exercise.html', exercises=exercises,name=name)






# back 
@app.route('/exercise-back-begineer')
def back_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("66196d7577ded31d89930aab")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Back Exercises'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-back-intermediate')
def back_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("66196d9677ded31d89930aac")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Back Exercises'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-back-advanced')
def back_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("66196db377ded31d89930aad")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Back Exercises'
    return render_template('exercise.html', exercises=exercises,name=name)






# chest 
@app.route('/exercise-chest-begineer')
def chest_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("661971c577ded31d89930ac0")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Chest'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-chest-intermediate')
def chest_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("661971e177ded31d89930ac1")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Chest'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-chest-advanced')
def chest_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("661971f477ded31d89930ac2")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Chest'
    return render_template('exercise.html', exercises=exercises,name=name)






# legs 
@app.route('/exercise-legs-begineer')
def legs_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("6619720e77ded31d89930ac3")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Legs'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-legs-intermediate')
def legs_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619723677ded31d89930ac4")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Legs'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-legs-advanced')
def legs_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("6619724a77ded31d89930ac5")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Legs'
    return render_template('exercise.html', exercises=exercises,name=name)






# abs 
@app.route('/exercise-abs-begineer')
def abs_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("6619726577ded31d89930ac6")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Abs'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-abs-intermediate')
def abs_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619727f77ded31d89930ac7")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Abs'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-abs-advanced')
def abs_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("6619729477ded31d89930ac8")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Abs'
    return render_template('exercise.html', exercises=exercises,name=name)







# cardiovascular 
@app.route('/exercise-cardiovascular-begineer')
def cardiovascular_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("661972ee77ded31d89930ac9")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Cardiovascular'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-cardiovascular-intermediate')
def cardiovascular_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619730377ded31d89930aca")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Cardiovascular'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-cardiovascular-advanced')
def cardiovascular_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("6619731877ded31d89930acb")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Cardiovascular'
    return render_template('exercise.html', exercises=exercises,name=name)







# strength training 
@app.route('/exercise-strength-begineer')
def strength_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("6619733077ded31d89930acc")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Strength Training'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-strength-intermediate')
def strength_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619734777ded31d89930acd")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Strength Training'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-strength-advanced')
def strength_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("6619735c77ded31d89930ace")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Strength Training'
    return render_template('exercise.html', exercises=exercises,name=name)






# flexibility and mobility 
@app.route('/exercise-flexibility-begineer')
def flexibility_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("6619737377ded31d89930acf")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Flexibility and Mobility'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-flexibility-intermediate')
def flexibility_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619738877ded31d89930ad0")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Flexibility and Mobility'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-flexibility-advanced')
def flexibility_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("661973b777ded31d89930ad1")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Flexibility and Mobility'
    return render_template('exercise.html', exercises=exercises,name=name)






# balance and stability 
@app.route('/exercise-balance-begineer')
def balance_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("661973f777ded31d89930ad2")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Balance and Stability'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-balance-intermediate')
def balance_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619740e77ded31d89930ad3")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Balance and Stability'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-balance-advanced')
def balance_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("6619742577ded31d89930ad4")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Balance and Stability'
    return render_template('exercise.html', exercises=exercises,name=name)






# core strength 
@app.route('/exercise-core-begineer')
def core_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("6619743c77ded31d89930ad5")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Core Strength'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-core-intermediate')
def core_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("6619745077ded31d89930ad6")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Core Strength'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-core-advanced')
def core_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("6619746477ded31d89930ad7")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Core Strength'
    return render_template('exercise.html', exercises=exercises,name=name)







# flat stomach
@app.route('/exercise-flat-begineer')
def flat_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("66196c6a77ded31d89930aa5")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Flat Stomach'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-flat-intermediate')
def flat_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("66196c8d77ded31d89930aa6")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Flat Stomach'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-flat-advanced')
def flat_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("66196caa77ded31d89930aa7")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Flat Stomach'
    return render_template('exercise.html', exercises=exercises,name=name)







# shoulders
@app.route('/exercise-shoulders-begineer')
def shoulders_begineer():
    exercise_doc = collection.find_one({"_id": ObjectId("66196cd777ded31d89930aa8")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Shoulders'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-shoulders-intermediate')
def shoulders_intermediate():
    exercise_doc = collection.find_one({"_id": ObjectId("66196cff77ded31d89930aa9")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Shoulders'
    return render_template('exercise.html', exercises=exercises,name=name)

@app.route('/exercise-shoulders-advanced')
def shoulders_advanced():
    exercise_doc = collection.find_one({"_id": ObjectId("66196d2177ded31d89930aaa")})
    if not exercise_doc:
        abort(404)  # Or handle the error in a way suitable for your application
    exercises = exercise_doc.get("exercises", [])
    name='Shoulders'
    return render_template('exercise.html', exercises=exercises,name=name)




if __name__=='__main__':
    app.run(debug=True,port=5000)