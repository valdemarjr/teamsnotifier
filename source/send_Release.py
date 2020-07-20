# -*- coding: utf-8 -*-

import pymsteams
import requests as req
import json
import os

def conn():
    try:
        conn = pymsteams.connectorcard(os.environ['WEBHOOK'])
        return conn
    except Exception as e:
        print("Connector Error: "+str(e))

def message_content(conn):
    try:
        message = conn
        # Definindo titulo da Mensagem
        message.title("Release %s.%s do projeto %s" % (os.environ['PROJECT_VERSION'],os.environ['BUILD_NUMBER'],os.environ['PROJECT_NAME']))
        message.text("Publicado no ambiente **%s**." % (os.environ['RELEASE_STAGE']))
        message.addLinkButton("Link para acesso ao ambiente %s." % (os.environ['RELEASE_STAGE']), os.environ['RELEASE_STAGE_URL'])
        
        # Create ChangeSet Section
        ChangeSetBody = os.environ['CHANGESET']
        ChangeSet = pymsteams.cardsection()
        ChangeSet.text(ChangeSetBody)

        # Create Authorizers Section
        Authorizers = pymsteams.cardsection()
        response = req.get("https://vsrm.dev.azure.com/%s/%s/_apis/release/releases/%s?api-version=5.0" % (os.environ['ORG_NAME'],os.environ['PROJECT_NAME'],os.environ['RELEASE_ID']), auth=(os.environ['VSTS_USER'], os.environ['VSTS_PAT']))
        try:
            AUTHORIZERS=json.dumps(response.json()['environments'][0]['preDeployApprovals'][0]['approver']['displayName'])
        except:
            AUTHORIZERS=os.environ['BUILDERS']
        Authorizers.text("Release criada por **%s** e autorizada por **%s**." % (os.environ['BUILDERS'],AUTHORIZERS))

        # Anexando 
        message.addSection(ChangeSet)
        message.addSection(Authorizers)
        
        return message
    except Exception as e:
        print("Message Content Error: "+str(e))
    

def message_send(message):
    try:
        message.send()
    except Exception as e:
        print("Sender Error: "+str(e))
    

def main():
    message_send(message_content(conn()))

if __name__ == '__main__':
    main()
    