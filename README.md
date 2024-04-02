# Weather Man

## Description
The Weather Man program calculates various weather statistics for a given year or month based on the provided weather data files. The statistics include the highest and lowest temperatures, the most humid day, and more. Additionally, the program can generate horizontal bar charts for the highest and lowest temperatures for each day of a given month, displaying them in red and blue, respectively.

## Modules Needed
- Python 3.9
- datetime
- argparse 1.4.0
- os
- re

## How to Run
```bash
python3 weatherman.py -e 2005/6 /path/to/files
python3 weatherman.py -a 2005/6 /path/to/files
python3 weatherman.py -c 2011/3 /path/to/files
```

## Output
1. For a given year:
   - Highest: 45°C on June 23
   - Lowest: 01°C on December 22
   - Most Humid: 95% on August 14

2. For a given month:
   - Highest Average: 39°C
   - Lowest Average: 18°C
   - Average Humidity: 71%

3. Example monthly chart (March 2011):
   ```
   01 +++++++++++++++++++++++++++++++++++ 11°C - 25°C
   02 +++++++++++++++++++++++++++++ 08°C - 22°C
   ...
   ```

## Validations and Functionality
- The program validates input arguments using the argparse library.
- It uses a generator function to read one file at a time, optimizing memory usage.
- Lambda functions are utilized to sort the data list by dates.
- The code adheres to PEP8 coding style guidelines.
- Proper exception handling is implemented for file-related operations.
