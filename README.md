# US Health Statistics Visualization (2014-2023)

An interactive visualization of US health statistics using CDC's Behavioral Risk Factor Surveillance System (BRFSS) data, presenting state-level health indicators across a decade.

## Overview

This project visualizes five key health indicators across all US states:
- General Health Status
- Heart Disease
- Stroke
- Cancer
- Arthritis

The visualization employs a grid map approach inspired by Nathan Yau's work, where each state is represented as an equal-sized unit to ensure unbiased data interpretation regardless of geographical size.

## Project Structure

```
us-health-statistics-visualization/
├── data_processing.py       # Script for processing Excel files into JSON
├── health_visualization.py  # Script for health data visualization
├── visualization.html
└── README.md
```

## Features

- **Equal-Area State Grid**: Each state is represented as an equal-sized unit
- **Multiple Health Indicators**: Visualization of five key health metrics
- **Gender Comparison**: Toggle between male and female statistics
- **Temporal Analysis**: Interactive year slider covering 2014-2023
- **Color Gradient Visualization**: Intuitive color scaling for prevalence rates

## Scripts

- `data_processing.py`: Processes multiple Excel files into a combined JSON format
- `health_visualization.py`: Handles the visualization logic and data transformation
- `visualization.html`: Contains the interactive visualization interface

## Data Source

The data is sourced from the [CDC's Behavioral Risk Factor Surveillance System (BRFSS)](https://www.cdc.gov/brfss/index.html), covering the years 2014-2023.

## Demo
You can view the live visualization here: https://deng34.github.io/us-health-statistics-visualization/visualization.html

## License

This project is licensed under the MIT License.

## Acknowledgments

- Inspired by Nathan Yau's grid map approach
- Data provided by CDC's Behavioral Risk Factor Surveillance System (BRFSS)