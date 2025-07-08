# app.py
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)

# Database configuration
def get_db_connection():
    conn = sqlite3.connect('employee_salary.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

# Load the trained model and preprocessor
try:
    model = pickle.load(open('models/salary_model.pkl', 'rb'))
    preprocessor = pickle.load(open('models/preprocessor.pkl', 'rb'))
except:
    # If model doesn't exist, train a new one
    model = None
    preprocessor = None

# Home page with form
@app.route('/')
def index():
    return render_template('index.html')

# Process form submission and make prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    age = float(request.form['age'])
    gender = request.form['gender'])
    education_level = request.form['education_level'])
    job_title = request.form['job_title'])
    years_of_experience = float(request.form['years_of_experience'])
    
    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'Education Level': [education_level],
        'Job Title': [job_title],
        'Years of Experience': [years_of_experience]
    })
    
    # Preprocess the input data
    processed_data = preprocessor.transform(input_data)
    
    # Make prediction
    predicted_salary = model.predict(processed_data)[0]
    
    # Store in database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO employees (age, gender, education_level, job_title, years_of_experience) VALUES (?, ?, ?, ?, ?)',
        (age, gender, education_level, job_title, years_of_experience)
    )
    employee_id = cursor.lastrowid
    cursor.execute(
        'INSERT INTO predictions (employee_id, predicted_salary) VALUES (?, ?)',
        (employee_id, predicted_salary)
    )
    conn.commit()
    conn.close()
    
    return render_template('results.html', 
                         predicted_salary=round(predicted_salary, 2),
                         age=age,
                         gender=gender,
                         education_level=education_level,
                         job_title=job_title,
                         years_of_experience=years_of_experience)

# View all employees
@app.route('/employees')
def view_employees():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

# Data visualization dashboard
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    
    # Get data for visualizations
    employees = pd.read_sql('SELECT * FROM employees', conn)
    predictions = pd.read_sql('SELECT * FROM predictions', conn)
    
    # Close connection
    conn.close()
    
    # Merge data
    data = pd.merge(employees, predictions, left_on='id', right_on='employee_id')
    
    # Create visualizations
    plots = {}
    
    # Salary distribution
    plt.figure(figsize=(10, 6))
    plt.hist(data['salary'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Salary Distribution')
    plt.xlabel('Salary')
    plt.ylabel('Count')
    salary_dist = plot_to_img()
    plots['salary_dist'] = salary_dist
    
    # Salary by education level
    plt.figure(figsize=(10, 6))
    data.groupby('education_level')['salary'].mean().sort_values().plot(kind='bar', color='lightgreen')
    plt.title('Average Salary by Education Level')
    plt.xlabel('Education Level')
    plt.ylabel('Average Salary')
    plt.xticks(rotation=45)
    salary_by_edu = plot_to_img()
    plots['salary_by_edu'] = salary_by_edu
    
    # Salary by job title
    plt.figure(figsize=(12, 6))
    data.groupby('job_title')['salary'].mean().sort_values().plot(kind='bar', color='salmon')
    plt.title('Average Salary by Job Title')
    plt.xlabel('Job Title')
    plt.ylabel('Average Salary')
    plt.xticks(rotation=90)
    salary_by_job = plot_to_img()
    plots['salary_by_job'] = salary_by_job
    
    # Salary vs Experience
    plt.figure(figsize=(10, 6))
    plt.scatter(data['years_of_experience'], data['salary'], alpha=0.5)
    plt.title('Salary vs Years of Experience')
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary')
    salary_vs_exp = plot_to_img()
    plots['salary_vs_exp'] = salary_vs_exp
    
    return render_template('dashboard.html', plots=plots)

# Helper function to convert plot to base64 image
def plot_to_img():
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f"data:image/png;base64,{plot_url}"

if __name__ == '__main__':
    app.run(debug=True)
