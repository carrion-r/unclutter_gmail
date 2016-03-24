
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from apiclient import errors

import time
import datetime
from datetime import date
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.labels']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'gmail-trash_deals.json')
    
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
    return credentials

def get_emails_with_label_and_before_date(service,user_id,label_name):
	try:
		
		query = 'label:'+label_name+' before:'+get_before_date()	
		response = service.users().threads().list(userId=user_id,q=query).execute()
		threads = response.get('threads',[])
		for email in threads:
			service.users().messages().trash(userId=user_id,id=email['id']).execute()
		
	except errors.HttpError,error:
		print('An error occurred: ',error)
	
def get_before_date():
	local_date = datetime.date.fromtimestamp(time.time())
	before_date_query = str(local_date.year)+'/'+str(local_date.month)+'/'+'0'
	return before_date_query
				
def main():
    """
    
    Creates a Gmail API service object. Then it fetches all the messages that are labeled 'deals' or 'travel'
    and are older than a month
    """
    credentials = get_credentials()
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    get_emails_with_label_and_before_date(service,'me','deals')
    get_emails_with_label_and_before_date(service,'me','travel')
    
	
	


if __name__ == '__main__':
    main()