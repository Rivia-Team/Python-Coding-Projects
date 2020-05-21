import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

def main():
    user_text = input("Please enter the text you want to listen: ")
    user_language = input("Please enter the E: English or S: Spanish: ").lower()
    print(f"here is the language {user_language}")

    if user_language == "e":
        user_voice = "Joanna"
        print(user_language)
        language_code = "en-US" 
        play_text(user_text,language_code, user_voice)
    elif user_language == "s":
        user_voice = "Lucia"
        language_code = "es-US" 
        play_text(user_text,language_code, user_voice)
    else:
        print(f"{user_language} is not a valid language. Please try again")
   

def play_text(user_text: str,language_code: str, user_voice: str ):
    session = boto3.Session(profile_name="pollyadmin")
    polly = session.client("polly")
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=user_text, OutputFormat="mp3",LanguageCode=language_code, VoiceId=user_voice)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream: # AudioStream: Stream containing the synthesized speech.
            # contextlib.closing(thing): Return a context manager that closes thing upon completion of the block.
            output = os.path.join(gettempdir(), "speech.mp3") # os.path.join(path, *paths): Join one or more path components
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file: # "w" - Write. "b" - Binary
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)
    
    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])


if __name__ == '__main__':
    main()
