import json


def get_data_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def total_videos(data):
    total_videos = len(data)
    print(f"Total videos {total_videos}")


def videos_per_channel(data):
    counter = dict()
    for video in data:
        channel = video["subtitles"][0]["name"]
        if channel not in counter:
            counter[channel] = 0
        counter[channel] += 1

    for key in counter:
        print(f"{key}: {counter[key]}")
