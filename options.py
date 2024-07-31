import tomllib


def location():
    with open("iclouded.toml", "rb") as f:
        config = tomllib.load(f)
        return config["options"]["location"]
