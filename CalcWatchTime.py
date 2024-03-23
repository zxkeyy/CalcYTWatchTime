import sys
import requests
import json
import datetime
import argparse
from tqdm import tqdm

API_KEY = "YOUR_API_KEY"
API_URL = "https://www.googleapis.com/youtube/v3/videos"
HISTORY_FILE = "watch-history.json"
MAX_VIDEOS_PER_REQUEST = 50

START_DATE = "2000-00-00T00:00:00Z"
MAX_DURATION = 5400  # 2 hours

SECONDS_IN_YEAR = 31536000
SECONDS_IN_MONTH = 2592000
SECONDS_IN_DAY = 86400
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60

parser = argparse.ArgumentParser(
        description="Calculate total watch time from YouTube watch history",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

parser.add_argument("-k", "--api-key", type=str, default=API_KEY, help="YouTube Data API V3 key")
parser.add_argument("-f", "--history-file", type=str, default=HISTORY_FILE, help="Path to the watch history JSON file")
parser.add_argument("-s", "--start-date", type=str, default=START_DATE, help="Start date in ISO 8601 format")
parser.add_argument("-d", "--max-duration", type=int, default=MAX_DURATION, help="Maximum duration of a video duration in seconds")

args = parser.parse_args()
config = vars(args)

API_KEY = config.get("api_key")
HISTORY_FILE = config.get("history_file")
START_DATE = config.get("start_date")
MAX_DURATION = config.get("max_duration")

def timeToSeconds(time):
    # Convert a time string in ISO 8601 format to seconds
    time = time[1:]  # Remove the 'P' at the start
    seconds = 0
    # Split into date and time components
    if 'T' in time:
        date, time = time.split('T')
    else:
        date = time
        time = ''

    if 'Y' in date:
        years, date = date.split('Y')
        seconds += int(years) * SECONDS_IN_YEAR
    if 'M' in date:
        months, date = date.split('M')
        seconds += int(months) * SECONDS_IN_MONTH
    if 'D' in date:
        days, date = date.split('D')
        seconds += int(days) * SECONDS_IN_DAY

    if 'H' in time:
        hours, time = time.split('H')
        seconds += int(hours) * SECONDS_IN_HOUR
    if 'M' in time:
        minutes, time = time.split('M')
        seconds += int(minutes) * SECONDS_IN_MINUTE
    if 'S' in time:
        seconds += int(time[:-1])

    return seconds

def getBatchVideosDuration(video_ids):
    # Get the duration of a batch of videos
    params = {
        "part": "contentDetails",
        "id": ",".join(video_ids),
        "key": API_KEY
    }

    # Make a request to the YouTube Data API
    try:
        response = requests.get(API_URL, params=params)
        response_json = response.json()
        if 'error' in response_json:
            print(response_json['error']['message'])
            raise Exception("An error occurred fetching video durations")
            return []
        # Extract the durations of the videos
        video_durations = [timeToSeconds(video['contentDetails']['duration']) for video in response_json['items']]

        return video_durations
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        raise Exception("An error occurred fetching video durations") from e  # Re-raise with context

def getVideosDuration(video_ids):
    # Get the duration of all videos in batches

    video_durations = []
    for i in tqdm(range(0, len(video_ids), MAX_VIDEOS_PER_REQUEST), desc="Getting video durations"): # tqdm is used to show a progress bar
        video_durations += getBatchVideosDuration(video_ids[i:i+MAX_VIDEOS_PER_REQUEST])

    return video_durations


# Load the watch history from a JSON file
with open('watch-history.json', 'r', encoding='utf-8') as file:
  watch_history = json.load(file)

# Extract the video IDs from the watch history
video_ids = []
deleted_videos = 0
for i in range(0, len(watch_history)):
    if 'titleUrl' not in watch_history[i]:
        deleted_videos += 1
        continue
    if watch_history[i]["time"] < START_DATE:
        break
    # Get the URL of the video
    video_url = watch_history[i]['titleUrl']
    # Extract the video ID from the URL
    video_ids.append(video_url.split('=')[-1])

# Get the duration of all videos
try:
  video_durations = getVideosDuration(video_ids)
except Exception as e:
  print(f"An error occurred processing watch history: {e}")
  exit()

# Cap the duration of each video at MAX_DURATION
for i in range(len(video_durations)):
    if video_durations[i] > MAX_DURATION:
        video_durations[i] = MAX_DURATION

# Calculate the total watch time in various units
total_time_seconds = sum(video_durations)
total_time_minutes = total_time_seconds / SECONDS_IN_MINUTE
total_time_hours = total_time_seconds / SECONDS_IN_HOUR
total_time_days = total_time_seconds / SECONDS_IN_DAY
total_time_months = total_time_seconds / SECONDS_IN_MONTH
total_time_years = total_time_seconds / SECONDS_IN_YEAR
total_time = str(datetime.timedelta(seconds=total_time_seconds))

# Print the results
print(f"Total time in seconds: {total_time_seconds}")
print(f"Total time in minutes: {round(total_time_minutes, 2)}")
print(f"Total time in hours: {round(total_time_hours, 2)}")
print(f"Total time in days: {round(total_time_days, 2)}")
print(f"Total time in months: {round(total_time_months, 2)}")
print(f"Total time in years: {round(total_time_years, 2)}")
print(f"Total time: {total_time}")
print(f"Total number of videos: {len(watch_history)}")
print(f"Number of deleted videos: {deleted_videos}")