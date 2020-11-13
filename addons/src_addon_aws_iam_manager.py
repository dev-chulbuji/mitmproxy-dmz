import boto3, json, threading, datetime
# import src_addon_logger as proxy_logger

class AWSThreadManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "AWSThread")
        self.period = 10
        self.client = boto3.client('iam')
        self.finished = threading.Event()
        self.key_to_user = {}

    def run(self):
        while not self.finished.is_set():
            self.get_users()
            self.finished.wait(self.period)

    def stop(self):
        self.finished.set()

    def get_users(self):
        rtv = {}

        response = self.client.list_users()
        for user in response["Users"]:
            username = user["UserName"]
            access_key_metas = self.get_access_key(username)

            for each in list(filter(lambda x: x["Status"] == 'Active', access_key_metas["AccessKeyMetadata"])):
                rtv[each["AccessKeyId"]] = username

        self.key_to_user = rtv

        ctx.log.info("complete to get users " + str(datetime.datetime.now()))

    def get_access_key(self, userName):
        access_keys = self.client.list_access_keys(UserName = userName)
        return access_keys

    def get_user_by_key(self, key):
        if len(self.key_to_user.values()) == 0:
            return ""

        if not key in self.key_to_user:
            return ""

        return self.key_to_user[key]

    def get_key_to_user(self):
        return self.key_to_user
