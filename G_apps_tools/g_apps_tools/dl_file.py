from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd

def google_auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    return GoogleDrive(gauth)

def dl_process(doc):
    drive = google_auth()
    if doc != "none":
        try:
            file = drive.CreateFile({'id': doc})
            file.GetContentFile('./doc/' + file['title'])
            return file["title"]
        except:
            return "none"
    else:
        return "none"

def download_file(doc_list):
    doc_list["doc_title"] = doc_list["file_id"].apply(dl_process)
    return doc_list

