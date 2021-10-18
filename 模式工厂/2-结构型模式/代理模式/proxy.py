class SensitiveInfo:
    def __init__(self):
        self.users = ["nick", "tom", "ben", "mike"]

    def read(self):
        print(f"There are {len(self.users)} users:{'、'.join(self.users)}")

    def add(self, user):
        self.users.append(user)
        print(f"Added user {user}")


class Info:

    def __init__(self):
        self.protected = SensitiveInfo()
        self.secret = "hypers"  # 秘钥

    def read(self):
        self.protected.read()

    def add(self, user):
        sec = input("what is the secret?")
        self.protected.add(user) if sec == self.secret else print("That's wrong!")


def main():
    info = Info()
    while True:
        print(" 1.read list \n 2.add user \n 3.quit")
        key = input("choose opt option:")
        if key == "1":
            info.read()
        elif key == "2":
            user = input("choose username:")
            info.add(user)
        elif key == "3":
            exit()
        else:
            print(f"unknown option {key}")


if __name__ == '__main__':
    main()
