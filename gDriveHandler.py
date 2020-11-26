from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import io, json
# For using listdir()
import os

class GAuth:

    def __init__(self):
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "/home/eigen/.gitwatch/client_secrets.json"
        self.cred_file = "/home/eigen/.gitwatch/local_credit.txt"
        self.stored_credentials = "/home/eigen/.gitwatch/local_credit.txt"

        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile(self.cred_file)

        if self.gauth.credentials is None:
            # Creates local webserver and auto
            # handles authentication.
            self.gauth.LocalWebserverAuth()
            self.gauth.SaveCredentialsFile(self.stored_credentials)
        self.drive = GoogleDrive(self.gauth)

    def writeJson(self, name, json_body):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            if file1["title"] == name:
                same_json_file = self.drive.CreateFile({'id': file1['id']})
                same_json_file.SetContentString(json.dumps(json_body))
                same_json_file.Upload()
                f = None
                return
        f = self.drive.CreateFile({'title': name})
        f.SetContentString(json.dumps(json_body))
        f.Upload()
        f = None


    def readJsonFile(self, name):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            if file1["title"] == name:
                same_json_file = self.drive.CreateFile({'id': file1['id']})
                return json.loads(same_json_file.GetContentString())

