import os
import random
import time
import httplib
import httplib2

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class MaxRetryExceeded(Exception):
    pass


class UploadFailed(Exception):
    pass

class Youtube:

    MAX_RETRIES = 10

    RETRIABLE_EXCEPTIONS = (
        httplib2.HttpLib2Error, IOError, httplib.NotConnected,
        httplib.IncompleteRead, httplib.ImproperConnectionState,
        httplib.CannotSendRequest, httplib.CannotSendHeader,
        httplib.ResponseNotReady, httplib.BadStatusLine
    )

    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    def __init__(self, secret_file: str, token_file: str):
        self.secret_file = secret_file
        self.token_file = token_file

        self.request = None
        self.response = None
        self.error = None
        self.retry = 0

    def get_authenticated_service(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.secret_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
                
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=creds)
    
    def initialize_upload(
            self,
            service,
            options
    ) -> dict:
        self.options = options

        body=dict(
            snippet=dict(
                title=options.title,
                description=options.description,
                tags=options.tags,
                categoryId=options.category
            ),
            status=dict(
                privacyStatus=options.privacyStatus,
                selfDeclaredMadeForKids=options.selfDeclaredMadeForKids
            )
        )

        media_body=MediaFileUpload(
            options.file,
            chunksize=-1,
            resumable=True
        )

        self.request = service.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media_body
        )
        self.resumable_upload()
        return self.response
    
    def resumable_upload(self):
        response = None
        while response is None:
            try:
                status, response = self.request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        self.response = response
                    else:
                        self.response = None
                        raise
            
            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    self.error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
                else:
                    raise UploadFailed("The file upload failed with an unexpected response:{}".format(response))

            except self.RETRIABLE_EXCEPTIONS as e:
                self.error = "A retriable error occurred: %s" % e

                if self.error is not None:
                    self.retry += 1

                    if self.retry > self.MAX_RETRIES:
                        raise MaxRetryExceeded("No longer attempting to retry.")

                    max_sleep = 2 ** self.retry
                    sleep_seconds = random.random() * max_sleep

                    time.sleep(sleep_seconds)