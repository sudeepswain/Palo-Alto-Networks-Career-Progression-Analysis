# Palo Alto Networks — Career Progression and Promotion Gap Analysis

## Project Overview

This project analyzes employee career progression, promotion gaps, training needs, manager stability, and retention opportunities at Palo Alto Networks.

The objective is to identify career stagnation patterns and provide data-driven insights that can support employee development and retention strategies.

## Dashboard Modules

- Executive Overview
- Career Path Clustering
- Promotion Gap Monitor
- Training Need Analysis
- Retention Opportunity
- Managerial Insights
- Employee Action Panel

## Analytical Methods

- Feature Engineering
- Standardization of Numerical Career Features
- K-Means Clustering
- Hierarchical Clustering Validation
- Promotion Gap Score
- Training Need Score
- Retention Opportunity Index
- Employee-Level Suggested Actions

## Dataset

The final analytical dataset contains:

- 1,470 employees
- 49 variables

## Project Quality Check

- Dataset rows: 1,470
- Dataset columns: 49
- Duplicate rows: 0
- Infinite numeric values: 0
- K-Means silhouette score: 0.2467
- Hierarchical silhouette score: 0.2210
- Adjusted Rand Index: 0.7399
- Retention opportunity population: 407
- Presentation figures: 15
- KPI consistency: Passed

## Technology

- Python
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Streamlit

## Running the Dashboard

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app.py
```