from base64 import b64decode
from csv import DictReader
from io import StringIO
from subprocess import run
from tempfile import TemporaryDirectory

from requests import get

with (StringIO(get("https://www.vpngate.net/api/iphone/").text) as csvfile,
      TemporaryDirectory() as temp):
    csvfile.seek(15)
    for row in DictReader(csvfile):
        if config := row.get("OpenVPN_ConfigData_Base64"):
            name = "{}-{}".format(row.get("CountryShort", "Unknown"), row["IP"])
            path = "{}/{}.ovpn".format(temp, name)
            with open(path, "w+b") as f:
                f.write(b64decode(config))
            run(["nmcli", "connection", "delete", name])
            run(["nmcli", "connection", "import", "type", "openvpn", "file", path])
