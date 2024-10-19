import sys
import stats

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            stats.total_stats(sys.argv[1], int(sys.argv[2]))
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
    else:
        print("Usage: script filepath threshold")
        print("script: filepath of the youtube watch history as .json file")
        print("threshold: threshold for the diagram. " +
              "Minimum number of videos viewed from a channel to show it in" +
              "the diagram")
