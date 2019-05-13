# Open311 Data Analysis

This project provides several methods for analyzing an Open311 data.

## Requirements

This project requires access to a database containing [Open311 Service](https://github.com/codeforamerica/open311status) data. You can set your database connection string in `data/__init__.py`

## Getting Started

Install the [required libraries](requirements.txt) and run main.py in your interpreter. By default, this generates a pie chart of requests for Peoria, Illinois.

To generate a different chart, open main.py and uncomment one of the commented function calls in the `main` function. To pull data for a specific city, replace the default city name with any one of the names listed in the `cities` table. 