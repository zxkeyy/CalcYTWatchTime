# YouTube Watch Time Calculator
This repository contains a Python script that calculates your total watch time from a YouTube watch history JSON file exported from YouTube Takeout. It leverages the YouTube Data API v3 to retrieve video durations and provides various time breakdowns.

# Features
- **Calculates total watch time:** Get a comprehensive overview of your YouTube viewing habits.
- **Handles deleted videos:** The script gracefully skips videos missing from your watch history due to deletion.
- **Customizable:** Set a start date to filter videos and a maximum video duration for capping outliers.
- **API Key Support:**  Requires a YouTube Data API v3 key for retrieving video durations.
- **Progress Bar:** Tracks progress while fetching video data.
- **Error Handling:** Includes basic error handling for API requests and JSON parsing.
- **Command-Line Interface:** Provides options to configure API key, history file path, start date, and maximum duration.

# Installation
Make sure you have the required libraries installed (requests, json, datetime, tqdm, argparse).  
You can use ```pip install requests json datetime tqdm argparse```

# Usage
1. Download your YouTube watch history as JSON from YouTube Takeout  
   **warning :** *it is important to click "multiple formats" and set the history format to JSON before creating the export*.
3. Update the ```API_KEY="YOUR_API_KEY"``` variable in the code with your ***YouTube Data API v3*** key or alternatively use the command line argument ```-k``` when running the code. You can create an API key at https://console.cloud.google.com/.
4. Run the script from the command line: CalcWatchTime.py (or adjust the filename if modified).

### Arguments
- ```-k``` : Your API key.
- ```-f``` : Path to your watch history JSON file (```"my_watch_history.json"``` by default)
- ```-s``` : The start date to count watched videos (```""2000-00-00T00:00:00Z"``` by default)
- ```-d``` : Maximum video duration in seconds, longer videos are capped at this duration to prevent outliers (2 hours by default)

### Example Usage

```python CalcWatchTime.py -k API_KEY -f downloads/watch-history.json -d 3600```

### Example Output:

```
Total time in seconds: 123456
Total time in minutes: 2057.60
Total time in hours: 34.29
Total time in days: 1.43
Total time in months: 0.05
Total time in years: 0.01
Total number of videos: 100
Number of deleted videos: 5
```

# Disclaimer:

This script relies on the YouTube Data API, which may have usage limits or change behavior in the future.
