#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os

from apiclient import errors
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import email
import base64
from email.mime.text import MIMEText
from email.header import Header
import mimetypes

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send'
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
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
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

def create_message(sender, to, subject, message_text): #Function used to create the a message with some kind of text using MIME structure.
    message = MIMEText(message_text, 'html')  # Creates the message
    message['to'] = to
    message['from'] = sender #passing the message information received as argument of the function
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())} # Returns the message encoded in a hash with the raw key

def create_draft(service, user_id, message_body): #Function used to create a draft, not used in this program.
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

        return draft
    except errors.HttpError, error:
        print('An error occurred: %s' % error)
        return None

def send_message(service, user_id, message): # Function used to send a single existing message (can be a created one or an already existing one from inbox for example)
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute()) 
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def ListMessagesMatchingQuery(service, user_id, query='{subject:currículo subject:cv subject:curriculum} newer_than:12m in:inbox'):  # This function is used to return a list of all messages where the subject is something about curriculum
    try:
        response = service.users().messages().list(userId=user_id,q=query).execute() # The actual query
        messages = [] # Create the array wich will store all the messages.
        if 'messages' in response:
            messages.extend(response['messages']) # Put the message in the end of the array (check if there is something).
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages']) #Same as above. But going to the next page of messages. If there is a nextPageToken, no need to check if there is a message.

        return messages
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def RedirectToLever(service, msg_id): #This function is used to redirect the message that has an attachment to the Lever e-mail.
    message = GetMimeMessage(service, 'me', msg_id) # Get the MIME message of a message by it's ID.
    message.replace_header('To', 'applicant@hire.lever.co') # Change the destination e-mail to the Lever e-mail.
    msg_raw = {'raw': base64.urlsafe_b64encode(message.as_string())} # Encode the new message.
    #send_message(service, 'me', msg_raw) #Send the message calling the send_message function.

def GetMimeMessage(service, user_id, msg_id): #This function returns the MIME message from a message id.

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute() #Search the message in the db from it's ID.

        #print(message)
        msg_str = base64.urlsafe_b64decode(message['raw'].decode('utf-8').encode('latin-1')) #Decode the message into a string.
        mime_msg = email.message_from_string(msg_str) # Function that convert the string generated into a MIME message structure that will be returned.
        return mime_msg
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def write_message():
    return ('Hey, tudo joia?<p></p><p></p>' 
        + 'Nós recebemos tantos currículos (mais de 5 mil!) no último'
        + ' semestre que foi preciso dar um up no nosso Banco de'
        + ' Talentos em 2017. Agora usamos uma plataforma muito'
        + ' fácil (e linda!) que diminui o risco do seu currículo'
        + ' ficar perdido no meio da multidão \o/ Lá você pode'
        + ' ver as vagas que estão abertas e se candidatar à '
        + 'que mais combina com você!<p></p><p></p>'
        + 'Esse é o link da nossa página de vagas: que.bo/vagas <p></p><p></p>' 
        + 'Ah, e se você já estiver trabalhando e quiser'
        + ' compartilhar o link com seus amigos, super pode'
        + ' (se não estiver trabalhando também pode compartilhar '
        + 'haha)! Vamos continuar crescendo e vamos precisar '
        + 'de muuuita gente pra acelerar o processo ^^<p></p><p></p>'       
        + 'Muito obrigada!<p></p><p></p>'
        + 'Um abraço,<p></p><p></p>'
        + 'Quero Educação')

def main(): # The main function to me executed.
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    '''results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name']) '''

    msg_to_be_send = write_message()
    sbj_to_be_send = Header('Novo caminho para trabalhar na Quero Educação ❤','utf-8')
    #msg1 = create_message('me','roger@redealumni.com', sbj_to_be_send, msg_to_be_send)
    #print(msg1['payload']['headers'])
    #print(msg1)
    #send_message(service, 'me', msg1)

    messages = ListMessagesMatchingQuery(service,'me',) # Get all messages about CV, as put in the declaration of the function above.
    senders = [] # Creates an array of the senders of messages about curriculum. We will send the text email to all e-mails in this array.
    fowarded = [] # Creates an array of emails that will be fowarded to the Lever email (messages with attachments).
    msgs_ids = [] # Array of messages ID's to be fowarded after de code runs.

    for msg in messages:
        msg_id = msg['id'] # Get the ID of the message.
        msg_txt = service.users().messages().get(userId='me', id=msg_id).execute() # Get the message as an structure. Better explained in the GMail API website: https://developers.google.com/gmail/api/v1/reference/users/messages
        gotSub = False
        gotSender = False
        headers = msg_txt['payload']['headers']
        for header in headers: # Iterate in the headers of the message (To, from, subject, etc...)
            try:
                if header['name'].lower() == "from": # This if is to find the "From" header, to get the email to where we will send the message.
                    sender = header['value']
                    gotSender = True
                if header['name'].lower() == "subject":
                    subject = header['value'] # This if is to find the "Subject" header, to get the email subject and check if it exists and if it's about curriculum. (Maybe this if is unnecessary)
                    gotSub = True
                if gotSender and gotSub: # If got both, we do all the job with the message.
                    if not fowarded.count(sender): # If we fowarded a message from this sender, there is nothing more to do with him/her.
                        for part in msg_txt['payload']['parts']: 
                            if part['filename']: # Check if there is an attachment in the message.
                                msgs_ids.append(msg_id) # Put the message in the array to be fowarded after
                                fowarded.append(sender) # Put this sender in the fowarded array.
                                if senders.count(sender) != 0 : # Remove the sender from the senders array.
                                    senders.remove(sender)
                                break
                        if senders.count(sender) == 0 and fowarded.count(sender) == 0: # If the message is not fowarded yet (the if above goes false), the message is not fowarded and isn't in the sender array.
                            senders.append(sender) # Put the e-mail in the senders array.
                    break
                #else:
                    #print(msg_txt['payload']['headers'][num]['name'].lower())
            except:
                # print('Something got wrong')
                break
    #for person in senders: #Finally, we iterate in the senders array to send the message to all the senders e-mails who didn't get fowarded to Lever.
        #msg1 = create_message('me', person, sbj_to_be_send, msg_to_be_send)
        #send_message(service, 'me', msg1)
        #print("Msg send to %s" % person)
    #for msgid in msgs_ids: #Iterate in msgs_ids to foward all the messages to Lever email
        #RedirectToLever(service, msgid) # Call redirect to Lever function for this message

    print(len(senders))
    print(len(fowarded))


if __name__ == '__main__':
    main()