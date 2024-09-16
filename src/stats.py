import json
import datetime
from matplotlib import pyplot as plt
from matplotlib import rcParams


def get_data_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def total_videos(data):
    return len(data)


def videos_per_channel(data):
    counter = dict()
    for video in data:
        channel = video["subtitles"][0]["name"]
        if channel not in counter:
            counter[channel] = 0
        counter[channel] += 1

    return counter


def threshold_videos_by_channel(counter, threshold):
    new_counter = dict()
    for channel in counter:
        if counter[channel] >= threshold:
            new_counter[channel] = counter[channel]

    return new_counter


def sort_videos_by_channel(counter):
    return sorted(counter.items(), key=lambda x:(-x[1], x[0]))


def get_datetime(date):
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


def get_oldest(data):
    date = get_datetime(data[len(data) - 1]["time"])
    return date.strftime("%Y-%m-%d %H:%M:%S")


def get_newest(data):
    date = get_datetime(data[0]["time"])
    return date.strftime("%Y-%m-%d %H:%M:%S")


def save_stats(data, threshold):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    frequency_per_channel = sort_videos_by_channel(videos_per_channel(data))
    diagram_name = f"frequency-per-channel_{current_time}"

    with open(f"statistics_{current_time}.md", "w", encoding="utf-8") as file:
        file.write("# Watch history statistics\n")
        file.write(f"Total videos: {total_videos(data)}\n\n")
        file.write(f"Total channels: {len(frequency_per_channel)}\n\n")
        file.write(f"Newest video: {get_newest(data)}\n\n")
        file.write(f"Oldest video: {get_oldest(data)}\n\n")

        file.write("## Videos per channel\n")
        for count, channel in enumerate(frequency_per_channel, 1):
            percentage = (channel[1] / total_videos(data))
            file.write(f"{count}. {channel[0]}: {channel[1]} ({percentage:.2%})\n")

        file.write(f"\n![]({diagram_name}.png)")

    create_diagram(dict(frequency_per_channel), threshold, diagram_name, data)


def create_diagram(frequency, threshold, name, data):
    counter = dict(threshold_videos_by_channel(frequency, threshold))
    x = list(counter.keys())
    y = list(counter.values())
    label_length = max([len(channel) for channel in counter])

    rcParams['font.family'] = ' Malgun Gothic'

    fig_size = plt.gcf().get_size_inches()
    plt.figure(figsize=(fig_size[0], fig_size[1] + label_length * 0.05))
    plt.style.use("fast")

    plt.title(f"Videos per channel (threshold: {threshold} --- {sum(y)}/{total_videos(data)})")
    plt.xlabel("Channel")
    plt.ylabel("Videos")

    plt.xticks(rotation=90)
    plt.yticks(y)
    plt.bar(x, y, width=0.75)
    plt.tight_layout()

    plt.savefig(name)


def total_stats(filename, threshold):
    data = get_data_from_file(filename)
    save_stats(data, threshold)
