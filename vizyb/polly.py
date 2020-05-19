# 9. task 15 - Write a program that takes the text you have provided
#    and returns an audio file in the language specified. Have the code ask the user
#    if they would like to play the file. Use AWS services for this exercise.
import argparse
import os
import subprocess
import sys
import boto3
import inquirer


def arguments():
    parser = argparse.ArgumentParser(description='''A program that takes the text you have provided
     and returns an audio file in the language specified''')
    parser.add_argument('--input_text', type=str, help='Text to synthesize.')
    parser.add_argument('--input_file', type=str, help='Path to text-file to synthesize.')
    parser.add_argument('--mp3', type=str, default='./speech.mp3', help='Where to store output mp3 file.')
    parser.add_argument('--audio', help='Whether to play result audio.', action='store_true')
    parser.add_argument('--select_lang', '--select_voice', help='Select language and voice.', action='store_true')
    return parser.parse_args()


def custom_lang_voice(voices):
    """ Parses available Polly configurations, prompts user, and returns choices """
    languages = {}
    for voice in voices["Voices"]:  # parse voices endpoint
        language = voice["LanguageName"]
        if languages.get(language) is not None:  # add languages to our dict
            languages.get(language).append(voice)
        else:
            languages[language] = [voice]

    selected_language = inquirer.prompt([inquirer.List('lang',
                                                       message='Which language?',
                                                       choices=languages.keys())])["lang"]
    language_code = languages[selected_language][0]["LanguageCode"]  # grab language code ie. en-US

    voice_keys = []
    for voice in languages[selected_language]:  # add available voices to list
        voice_keys.append(voice["Id"])

    selected_voice = inquirer.prompt([inquirer.List('voice',
                                                    message='Which voice?',
                                                    choices=voice_keys)])["voice"]

    return language_code, selected_voice


def main():
    speech_text = None
    args = arguments()
    try:
        if args.input_text is not None:
            speech_text = args.input_text
        elif args.input_file is not None:
            with open(args.input_file) as text_file:
                speech_text = text_file.read()
        if not speech_text:
            raise RuntimeError("Please provide input text or input file.")

        polly_client = boto3.Session(profile_name="default").client('polly')

        language = "en-US"
        voice = 'Joanna'
        if args.select_lang:
            voices = polly_client.describe_voices()  # returns dict
            custom_choice = custom_lang_voice(voices)
            language = custom_choice[0]
            voice = custom_choice[1]

        response = polly_client.synthesize_speech(VoiceId=voice,
                                                  LanguageCode=language,
                                                  OutputFormat='mp3',
                                                  Text=speech_text)

        with open(args.mp3, 'wb') as mp3_file:
            mp3_file.write(response['AudioStream'].read())

        if args.audio:
            # Play the audio using the platform's default player
            if sys.platform == "win32":
                os.startfile(args.mp3)
            else:
                # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, args.mp3])

    except PermissionError as permission_error:
        print(permission_error)
    except Exception as general_error:
        print(general_error)


if __name__ == "__main__":
    main()
