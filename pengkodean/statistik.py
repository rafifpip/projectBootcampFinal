from collections import Counter

def count_classes(detections):

    counter = Counter()

    for item in detections:

        counter[item["class"]] += 1

    return dict(counter)