# employee_salary_app-
Employee Salary Prediction Web Application
create a comprehensive web application for employee salary prediction based on the provided Jupyter notebook. This will include:

A SQL database to store employee data

A web interface for inputting employee details

Salary prediction functionality

Data visualization and analysis tools




## 🗃️ Database Design (SQL)

The application uses a simple relational database schema to store employee data and their salary predictions.



```sql
-- Database: employee_salary

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age FLOAT,
    gender VARCHAR(10),
    education_level VARCHAR(50),
    job_title VARCHAR(100),
    years_of_experience FLOAT,
    salary FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    predicted_salary FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
```




# 🧑‍💼 Employee Salary Prediction App

A Flask-based web application to predict employee salaries, view all employees, and visualize data through an interactive dashboard.

## 📁 Project Structure

```bash
employee_salary_app/
├── app.py                 # Main application file
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page with form
│   ├── results.html       # Prediction results
│   ├── dashboard.html     # Data visualization dashboard
│   └── employees.html     # View all employees
├── static/
│   ├── css/
│   │   └── styles.css     # Custom styles
│   └── js/
│       └── scripts.js     # Custom JavaScript
├── models/
│   ├── salary_model.pkl   # Trained model
│   └── preprocessor.pkl   # Data preprocessor
└── requirements.txt       # Python dependencies
```





## 🚀 Features

- Predict salary using machine learning
- Store and view employee records
- Visualize data in a dashboard
- Clean, modular structure for scalability

## 🔧 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/employee_salary_app.git
   cd employee_salary_app
