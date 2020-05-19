"""
task 15 - Write a program that takes the text you have provided
   and returns an audio file in the language specified. Have the code ask the user
   if they would like to play the file. Use AWS services for this exercise.
"""

import boto3
from contextlib import closing
import os

VOICE = "Joey"
LANGUAGE_OPTIONS = {
    "arb": "Arabic",
    "cmn-CN": "Chinese",
    "da-DK": "Danish",
    "es-US": "English",
    "fr-FR": "French",
    "de-DE": "German",
    "pl-PT": "Portugese",
    "es-ES": "Spanish"
}

def introduction():
    """
    Introduces the program to the user and gets the text they would
    like turned into an audio file and the language they want
    :return: user_input as a string and user_language as a string
    """
    print("Hello, this is a simple program that will convert your input")
    print("into an audio file and play it for you.")
    user_input = input("What audio would you like to hear? ")
    print("What language would you like?")
    print("For Arabic enter: 'arb'")
    print("For Chinese enter: 'cmn-CN'")
    print("For Danish enter: 'da-DK'")
    print("For English enter: 'es-US'")
    print("For French enter: 'fr-FR'")
    print("For German enter: 'de-DE'")
    print("For Portuguese enter: 'pl-PT'")
    print("For Spanish enter: 'es-ES'")
    get_language = input("Enter your choice: ")
    if validate_lang(get_language):
        user_language = get_language
        print("Success, your language is: " + LANGUAGE_OPTIONS[get_language])
    else:
        user_language = "es-US"
        print("Input is not valid, language set to English.")

    return user_input, user_language


def validate_lang(lang):
    """
    valids user input for language
    :param lang: language to valid
    :return: True if language is valid
    """
    if lang in LANGUAGE_OPTIONS.keys():
        return True


def generate_audio():
    """
    Generates the audio file
    :return:
    """
    text, lang = introduction()
    ses = boto3.Session(profile_name="default")
    pol = ses.client("polly")
    res = pol.synthesize_speech(Text=text, LanguageCode=lang, OutputFormat="mp3", VoiceId=VOICE)
    return res


def create_audio_file():
    """
    creates the audio file from the user input
    :return:
    """
    # Get the response from boto3
    raw_audio = generate_audio()
    # pull the Audiostream object from the response from boto3
    raw_audio = raw_audio["AudioStream"]
    # create output location
    # process the whole block
    with closing(raw_audio) as audio:
        with open("output_audio.mp3", "wb") as file:
            file.write(raw_audio.read())


def play_audio():
    """
    Plays the audio file
    :return:
    """
    play_file = input("Would you like to play the file we created (y/n)? ")
    if play_file == "y":
        os.system("open output_audio.mp3")
    else:
        print("Thanks for using our service, the file exists in your directory where you ran this file.")


def main():
    create_audio_file()
    play_audio()


if __name__ == "__main__":
    main()