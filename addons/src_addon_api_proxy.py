from mitmproxy import ctx, http, log

# from src_addon_aws_iam_manager import AWSThreadManager
from datetime import datetime

import src_addon_config as config
import src_addon_logger as proxy_logger
import re, json, sys, signal

class AwsApiCallProxy:
    def __init__(self):
        # self.aws_thread_manager = AWSThreadManager()
        # self.aws_thread_manager.start()

        # graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
            
    def signal_handler(self, signal, frame):
        """
        # self.aws_thread_manager.stop()
        """

    def load(self, loader):
        for each in config.addon_configs:
            loader.add_option(                
                name = each["name"],
                typespec = each["typespec"],
                default = each["default"],
                help = each["help"]
            )
    
    def configure(self, updated) -> None:
        """
        ctx.log.info('options: %s' % ctx.options.verbose)
        """

    def requestheaders(self, flow) -> None:
        http_version = flow.request.http_version
        host = ""

        if http_version == "HTTP/1.1":
            host = flow.request.headers["Host"]
        else:
            host = flow.request.host
            flow.kill()

        check = self.check_request_host_by_whitelist(host)

        if not check:
            ctx.log.info("%s | filter non aws api call: hsot=%s" % (datetime.now(), host))
            flow.kill()
            return

        is_aws_api, accesskey = self.check_aws_api_call(flow.request.headers)
        
        # if is_aws_api == True:
        #     if not self.check_access_key(accesskey):
        #         ctx.log.info("%s | not exist accesskey | host=%s, accesskey=%s" % (datetime.now(), host, accesskey))
        #         self.send_blocked_response(flow)
        #         return

        
        self.print_log(host, accesskey)

    def request(self, flow) -> None:
        """
        body = flow.request.content
        """

    def response(self, flow) -> None:
        """
        """

###########################################################################################################

    def print_log(self, host, accesskey):
        # user = self.aws_thread_manager.get_user_by_key(accesskey)
        ctx.log.info("%s | request info :: accesskey=%s, host=%s" % (datetime.now(), accesskey, host))

    def check_request_host_by_whitelist(self, host):
        rgx = ctx.options.filterurl
        p = re.compile(rgx)
        m = p.match(host)

        return m

    def check_aws_api_call(self, headers):
        """
            check if request is aws api call or not
            - check request got 'authorization' header field
            - check credential get access key & aws4_request
            - ex :: aws4-hmac-sha256 credential=akia2rh2pmnigv7dpq4a/20190823/ap-northeast-2/s3/aws4_request
        """
        if not "authorization" in headers:
            return False, ""
    
        pattern = re.compile(r".*Credential=([^,]+)")
        matched = pattern.match(headers['authorization'])
    
        if matched == None:
            return False, ""
    
        splitted = matched.group(1).split('/')
    
        if splitted[-1] != 'aws4_request':
            return False, ""
    
        accesskey = splitted[0]
        return True, accesskey
    
    # def check_access_key(self, key):
    #     key_to_user = self.aws_thread_manager.get_key_to_user()
    #
    #     if len(key_to_user.values()) == 0:
    #         return False
    #
    #     return key in key_to_user

    def send_blocked_response(self, flow):
        flow.response = http.HTTPResponse.make(
            403,  # (optional) status code
            b"request not allowed",
            {"content-type": "content-type: text/html; charset=utf-8"}
        )

    def log(self, e):
        proxy_logger.info(json.dumps(e.msg))

addons = [
    AwsApiCallProxy()
]
