"""
Task
- Write a program that takes the text you have provided

and returns an audio file in the language specified. Have the code ask the user

if they would like to play the file. Use AWS services for this exercise.

PreReqs: Go to Linux Academy and setup an AWS console.  Copy the ACCESS
and SECRET key into the ~/.aws/credentials file like so:

[default]
aws_access_key_id= <ACCESS KEY>
aws_secret_access_key= <SECRET KEY>

and the ~/.aws/config file as:
[default]
region=us-east-1
output=json


https://docs.aws.amazon.com/polly/latest/dg/get-started-what-next.html
"""

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys

POLLY_CHAR_LIMIT = 3000

def polly_request_speech(intext: str, intlanguage: str):
    """ Request Polly speech given text and language."""
    session = Session(profile_name="default")
    polly = session.client("polly")
    try:
        response = polly.synthesize_speech(Text=intext,LanguageCode = intlanguage,OutputFormat="mp3",VoiceId="Joanna")
        print(response)
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(1)
    return response


def polly_write_response(inresponse: object):
    """ Write the response of the Polly request. """
    if "AudioStream" in inresponse:
        with closing(inresponse["AudioStream"]) as stream:
            output = os.path.join(os.getcwd(), "speech.mp3")
            print(output)
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(1)
    else:
        print("Could not stream audio")
        sys.exit(1)


def get_user_text() -> str:
    """ Ensure the user request can go to Polly. """
    validinput = False
    while not validinput:
        intext = input("Which of your most favorite quotes can Polly cook up for you?")
        if len(intext) > POLLY_CHAR_LIMIT:
            print("You have entered in more text that Polly can support in one call.")
            validinput = False
        else:
            validinput = True
    return intext

def get_audio_file():
    os.system("open speech.mp3")

def get_user_language() -> str:
    """ Allow the user to choose from a pre-defined set of languages. """
    languages = {
        "arabic": "arb",
        "chinese": "cmn-CN",
        "danish": "da-DK",
        "english": "en-GB",
        "french": "fr-FR",
        "german": "de-DE",
        "portuguese": "pl-PT",
        "spanish": "es-ES"
    }
    textlang = input("What language do you want to hear?")
    try:
        return languages[textlang.lower()]
    except KeyError as e:
        print("Enter a valid language.")
        sys.exit(1)

def main():
    requesttxt = get_user_text()
    requestlang = get_user_language()
    myspeech = polly_request_speech(requesttxt, requestlang)
    polly_write_response(myspeech)
    get_audio_file()


if __name__ == "__main__":
    main()
