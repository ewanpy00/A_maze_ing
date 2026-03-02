def process_arguments():
    result = dict()
    with open("config.txt") as ds:
        for line in ds:
            line = line.strip()
            key, value = line.split("=")
            result[key] = value

    return result
