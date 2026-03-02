# 🚴 Data Analysis Final Project - DEPI Round 4

## 📌 Project Overview

This project focuses on analyzing bike-sharing trip data to extract meaningful insights about user behavior, trip patterns, and station usage.

The project includes:

* Data Cleaning & Preprocessing
* Exploratory Data Analysis (EDA)
* Feature Engineering
* Data Encoding & Scaling
* Interactive Dashboard using Plotly Dash

---

## 📂 Dataset

The dataset contains trip records including:

* Trip duration
* Start & end stations
* User type (Subscriber / Customer)
* Gender
* Birth year

### 🔗 Data Sources

* Original Data:
  https://drive.google.com/file/d/1cSi6X4MA-70K4SMQz42y_SFwFhd6KJXH/view?usp=drive_link

* Cleaned Data:
  https://drive.google.com/file/d/179fZPkinz8rIrozG2OFeslnF44AGZ9BD/view?usp=sharing

---

## 🧹 Data Preprocessing

Steps applied to clean the dataset:

* Removed duplicate records
* Handled missing values:

  * Numerical → Median
  * Categorical → Mode / "Unknown"
* Removed outliers using IQR method
* Standardized categorical values:

  * `user_type`
  * `member_gender`
  * `bike_share_for_all_trip`

---

## ⚙️ Feature Engineering

New features were created:

* `duration_min` → Trip duration in minutes
* `age` → Calculated from birth year
* `age_group` → Categorized into:

  * Young (0–25)
  * Adult (26–40)
  * Middle Age (41–60)
  * Senior (60+)

---

## 🔢 Encoding & Scaling

* Label Encoding:

  * `user_type`
  * `bike_share_for_all_trip`

* One-Hot Encoding:

  * `member_gender`

* Feature Scaling:

  * `age`
  * `duration_min`

---

## 📊 Exploratory Data Analysis (EDA)

Key insights:

* Most trips are short (right-skewed distribution)
* Subscribers dominate the system usage
* Male users have the highest number of trips
* Customers tend to have longer trip durations
* Younger users generally take shorter trips

---

## 📈 Dashboard (Plotly Dash)

An interactive dashboard was built with:

### 🎛 Filters

* User Type
* Gender
* Age Group

### 📌 KPIs

* Total Trips
* Average Duration
* Active Users
* Most Popular Station

### 📊 Visualizations

* Subscriber vs Customer usage
* Gender distribution
* Trip duration distribution
* Top start stations
* Top end stations

---

## ▶️ How to Run the Dashboard

1. Install requirements:

```bash
pip install pandas plotly dash dash-bootstrap-components
```

2. Run the app:

```bash
python app.py
```

3. Open in browser:

```
http://127.0.0.1:8050/
```

---

## 🧠 Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib & Seaborn
* Plotly
* Dash
* Scikit-learn

---

## 🚀 Future Improvements

* Add time-based analysis (peak hours)
* Add geospatial map visualization
* Deploy dashboard online
* Add machine learning prediction model

---

## 👨‍💻 Authors

**Mostafa Gamal Fouda**

**Mariam Gaber**

**Abdelhamid Ebrahim** 

**Tasneem Radwan**

**Mostafa Fathallah**

**Samuel Adel**

Machine Learning Engineer | DEPI trainees

---
