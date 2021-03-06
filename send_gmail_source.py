#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''

   The full program is explained in the attached ReadMe.md

    Copyright (C) 2013 warehouseman.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Created on 2014-09-15

    @author: Martin H. Bramwell

    This module:
       This is a helper program to allow you to send emails to through your
       your GMail account.

'''
import os
import urllib
import logging
import argparse

import loadGoogleJSON

try :

    from goauth2_helper import GeneratePermissionUrl
    from goauth2_helper import AuthorizeTokens
    from goauth2_helper import GenerateOAuth2String
    from goauth2_helper import RefreshToken
    
except ImportError :

    # Get Google oauth2 helper file
    webFile = urllib.urlopen('http://google-mail-oauth2-tools.googlecode.com/svn/trunk/python/oauth2.py')
    localFile = open('goauth2_helper.py', 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    
    from goauth2_helper import GeneratePermissionUrl
    from goauth2_helper import AuthorizeTokens
    from goauth2_helper import GenerateOAuth2String
    from goauth2_helper import RefreshToken

import smtplib
import base64
import re

import traceback
import datetime

parameters_file = 'working_parameters.py'

SMTP_ACCESS = 'google_project_client_smtp_access_token'
SMTP_REFRESH = 'google_project_client_smtp_refresh_token'
SMTP_EXPIRY = 'google_project_client_smtp_expiry'
CLIENT_EMAIL = 'google_project_client_email'
configure_email = False

gpcsat_len = 0
gpcsrt_len = 0
try:

    from working_parameters import google_project_client_smtp_access_token
    from working_parameters import google_project_client_smtp_refresh_token
    
    gpcsat_len = len(google_project_client_smtp_access_token)
    gpcsrt_len = len(google_project_client_smtp_refresh_token)
    
    assert gpcsat_len > 50 and gpcsat_len < 80
    assert gpcsrt_len == 45

except :

    configure_email = True
    print 'No valid token pair found in {}. Will run the wizard.'.format(parameters_file)
#    print 'Lengths : Access Token = {}, Refresh Token = {}.'.format(gpcsat_len, gpcsrt_len)

import fileinput
def update_parms_file(acc, ref, exp, cgm):

    acc_parm = "%s = '%s'" % (SMTP_ACCESS, acc)
    a = True
    
    ref_parm = "%s = '%s'" % (SMTP_REFRESH, ref)
    r = True
    
    exp_parm = "%s = '%s'" % (SMTP_EXPIRY, exp)
    x = True
    
    cgm_parm = "%s = '%s'" % (CLIENT_EMAIL, cgm)
    g = True
    
    
    for line in fileinput.input(parameters_file, inplace=1):
      if line.startswith(SMTP_ACCESS) :
          print acc_parm
          a = False
      elif line.startswith(SMTP_REFRESH) :
          print ref_parm
          r = False
      elif line.startswith(SMTP_EXPIRY) :
          print exp_parm
          r = False
      elif line.startswith(CLIENT_EMAIL) :
          print cgm_parm
          g = False
      else :
          print line,
    
    if a or r or x:
        with open(parameters_file, "a") as myfile:
            myfile.write('\n# Appended automatically . . . ')
            if a :
                myfile.write('\n%s' % acc_parm)
            if r :
                myfile.write('\n%s' % ref_parm)
            if x :
                myfile.write('\n%s' % exp_parm)
            if g :
                myfile.write('\n%s' % cgm_parm)
            myfile.write('\n#\n')
       
              
def prep_smtp(creds, client_email, test_mail = False) :

    if client_email == None:
      try:
      
          from working_parameters import google_project_client_email
          
      except ImportError:

          google_project_client_email = raw_input('Enter the GMail address you want to authorize : ')
          if not re.match("[^@]+@[^@]+\.[^@]+", google_project_client_email):
            print 'Bad email.  Try again, or you can edit "{0}.example" and save as "{0}" before running the tests.'.format(parameters_file)
            exit(-1)
            
    else :
      google_project_client_email = client_email

    
    expiry = ''
    if configure_email :
    
        scope = 'https://mail.google.com/'

        print "\n    To be able to request authorization from your users by email, you need to authorize this program to use Google's email resender in your name."
        print "    Visit this url and follow the directions:\n"
        print '  %s' % GeneratePermissionUrl(
                                                  creds.installed.client_id
                                                , scope
                                            )
        authorization_code = raw_input('\n\n    * * * Enter verification code: ')

        response = AuthorizeTokens  (
                                          creds.installed.client_id
                                        , creds.installed.client_secret
                                        , authorization_code
                                    )
        access_token = ''
        refresh_token = ''
            
        try :
            access_token = response['access_token']
            refresh_token = response['refresh_token']
        except :
            print '\n\nServer reported   %s' % response
            print ' - Did you get the *latest* verification code?'
            print ' - Did you get all of it?'
            print ' - Did you use exactly the right ID and Secret for "Client for Installed Applications" from the Google API Console?\n(https://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&ved=0CC4QFjAA&url=http%3A%2F%2Fcode.google.com%2Fapis%2Fconsole&ei=RgdEUvu-GM754AOeh4GgAQ&usg=AFQjCNFikY2jzXn9SOuZu0UcyS-59LlsTw&sig2=hpYvu7CrTb8royXO9f3nyQ&bvm=bv.53217764,d.dmg)'
            exit(-1)
        
        expiry = (datetime.datetime.now() + datetime.timedelta(0,response['expires_in'])).strftime('%Y-%m-%d %H:%M')
        print '\nSuccess :'
        print ' - Access Token: = %s' % access_token
        print ' - Refresh Token: %s'% refresh_token
        print ' - Access Token expires at : %s' % expiry

        
        print 'Appending latest tokens to the bottom of the file "{}". . . '.format(parameters_file)
        update_parms_file(access_token, refresh_token, expiry, google_project_client_email)
        print ' . . done.\n'
            
        
    else :
    
        print 'An SMTP access token pair is already registered in "{}"'.format(parameters_file)
        access_token = google_project_client_smtp_access_token
        refresh_token = google_project_client_smtp_refresh_token    

    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.set_debuglevel(False)
    smtp_conn.ehlo('test')
    smtp_conn.starttls()
            
    # Temporary token...
    auth_string = GenerateOAuth2String  (
                                              google_project_client_email
                                            , access_token
                                            , base64_encode = False
                                        )
    ### print auth_string
    
    # Preparing test email envelope . . 
    title = 'Trash this email'
    body = 'Congratulations. You have fully enabled mail transfer through Google SMTP.'
    envelope = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (
                  google_project_client_email
                , google_project_client_email
                , title
                , body)
 
    if test_mail :
        print ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print envelope
        print ' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            
        try :
        
            smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string))
            print 'Sending . . . '
            smtp_conn.sendmail(google_project_client_email, google_project_client_email, envelope)
            print '. . . sent!\n'
            
        except smtplib.SMTPSenderRefused as sr :
            if sr[0] == 530 :
                print 'Refresh required: Using %s' % refresh_token
                access_token = RefreshToken(creds.installed.client_id, creds.installed.client_secret, refresh_token)
                print 'New token : %s' % access_token
                smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string))
                
                try :
                        smtp_conn.sendmail(google_project_client_email, google_project_client_email, envelope)
                except smtplib.SMTPSenderRefused as sr :
                    print sr
                    if sr[0] == 535 :
                        print 'The access token is correct. Maybe the user id is wrong?'
                        print '¿ Are you sure that <[{0}]> authorized <[{0}]> ?'.format(google_project_client_email)
                        exit(-1)


    
    else :
        print 'No test mail sent.'
    
    return



pth = os.path.realpath(__file__)
PROG = pth.split(os.sep)[pth.count(os.sep)]

desc = 'Get the access and refresh tokens for SMTP access to your GMail account.'
desc += '  The values are added to the file {}.'.format(parameters_file)
desc += '  If file {} already have all the necessary parameters no'.format(parameters_file)
desc += ' action is taken.'

'''
msg_c = "to drop and create new credentials"
msg_k = "The identity key of a Google Spreadsheets workbook."
msg_r = "Row in Tasks sheet at which to start processing."
'''

def get():

    usage = "usage: {} [options] arg".format(PROG)
    parser = argparse.ArgumentParser(description=desc, prog=PROG)
    
    msg_j = 'A json file of Google OAuth credentials from '
    msg_j += 'https://console.developers.google.com/ » [APIs & auth] » '
    msg_j += '[Credentials] » [Client ID for native application]'
    parser.add_argument(
        '-j'
      , '--client_id_json'
      , help=msg_j
      , required=False
    )
    parser.add_argument(
        '-e'
      , '--client_email'
      , help='Your full GMail address [e.g. your.addr@gmail.com]'
      , default=None
      , required=False
    )
    parser.add_argument(
        '-m'
      , '--test_mail'
      , help='Send a test email? (True|False) Default = False'
      , default=False
      , required=False
    )

    return parser.parse_args()


    
def main():
    
    args = get()

    creds = loadGoogleJSON.getCreds(args.client_id_json)
    if creds != None:
      open(parameters_file, 'a').close()
      oauth_credentials = prep_smtp(creds, args.client_email, args.test_mail)
    return

if __name__ == '__main__':

    logging.FileHandler('python.log', mode='a')
    logger = logging.getLogger(PROG)
    logger.setLevel('DEBUG')
#    logger.setLevel('WARNING')

    main()
    exit(0)


