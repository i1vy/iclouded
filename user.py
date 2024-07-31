from icloudpy import ICloudPyService
import sys
import tomllib


def username():
    with open("iclouded.toml", "rb") as f:
        config = tomllib.load(f)
        return config["user"]["username"]


def password():
    with open("iclouded.toml", "rb") as f:
        config = tomllib.load(f)
        return config["user"]["password"]


def authenticate():
    api = ICloudPyService(username(), password())

    if api.requires_2fa:
        print("2fa required :<")
        print("you should get a code on a device or something")
        code = input("enter code: ")
        result = api.validate_2fa_code(code)
        print("did it work? find out here -> %s" % result)

        if not result:
            print("failed to verify")
            sys.exit(1)

        if not api.is_trusted_session:
            print("requesting trust...")
            result = api.trust_session()
            print("trust: %s" % result)

            if not result:
                print("no trust? idk how this works")

    return api
