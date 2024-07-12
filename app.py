from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoints():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # Retrieve form data
        gender = request.form.get('gender')
        ethnicity = request.form.get('ethnicity')
        parental_level_of_education = request.form.get('parental_level_of_education')
        lunch = request.form.get('lunch')
        test_preparation_course = request.form.get('test_preparation_course')
        
        # Handle optional fields with default values or None
        reading_score_str = request.form.get('reading_score')
        writing_score_str = request.form.get('writing_score')
        
        # Convert scores to integers, handling None gracefully
        reading_score = int(reading_score_str) if reading_score_str else None
        writing_score = int(writing_score_str) if writing_score_str else None
        
        # Create CustomData object
        data = CustomData(
            gender=gender,
            race_ethnicity=ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        # Example: initialize PredictPipeline and make prediction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        # Pass results to home.html for display
        return render_template('home.html', results=results[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)