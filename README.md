# SkySage-Navigating-Delays-with-Data-driven-Precision


![Flight Delays](https://github.com/saikumar28102000/SkySage-Navigating-Delays-with-Data-driven-Precision/blob/main/white-alarm-clock-airplane-background-viva-magenta.jpg)

Welcome to the Flight Delay Prediction Project! This repository contains the code and resources for a machine learning project focused on predicting departure delays caused by adverse weather conditions at major US airports. By combining historical flight data and real-time weather information, the project aims to enhance the accuracy of delay predictions, optimize operational efficiency, and improve customer satisfaction within the airline industry.

## Table of Contents

- [Project Overview](#project-overview)
- [Phases](#phases)
- [Getting Started](#getting-started)
- [Contributions](#contributions)
- [License](#license)
- [Contact](#contact)

## Project Overview

Flight delays have a significant impact on airlines, passengers, and operational costs. This project addresses the challenge of predicting departure delays by leveraging machine learning algorithms and real-time weather data. The project is divided into three main phases:

### Phases

1. **Dataset Formation and ETL**: This phase involves creating a robust ETL pipeline using Azure Data Factory. Data is extracted from the Open Weather API and the Aviation Stack API, transformed, cleaned, and merged into a comprehensive dataset.
   
2. **Regression Models**: Various regression models, including Linear Regression, K-Neighbors Regressor, Decision Tree Regressor, Random Forest Regressor, and XGBoost, are explored. Model performance is evaluated using metrics such as RMSE, MAE, and R-squared. The top-performing model is the XGBoost model with hyperparameter tuning.

3. **Website Development and Interaction**: The final phase focuses on creating an interactive web interface using Flask and HTML. Users can input parameters like date, origin, and destination, and the application provides real-time departure delay predictions. This user-friendly platform empowers airlines and passengers with valuable insights for planning.

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine using the following command:
   ```
   git clone https://github.com/yourusername/SkySage-Navigating-Delays-with-Data-driven-Precision.git
   ```

2. Install the required libraries and dependencies using:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```
   python app.py
   ```

