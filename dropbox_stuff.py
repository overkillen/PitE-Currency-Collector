import json

import dropbox


class DBClient:
    token = '4F7nibHK-YAAAAAAAAAABqk5WWYBQYAdXBDkTdg4LImkLa0GE3IQ0b7iyVcKPdT3'

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = dropbox.Dropbox(self.token)
        return self._client

    def __init__(self, token=None):
        if token is not None:
            self.token = token

    def upload_file(self, content, filename='/currency_dump.json'):
        self.client.files_upload(content.encode("utf-8"), filename)
        return True

    def download_file(self, filename='/currency_dump.json'):
        metadata, resp = self.client.files_download(filename)
        return resp.content.decode("utf-8")

