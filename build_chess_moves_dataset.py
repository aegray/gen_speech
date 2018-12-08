import os
import time

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import texttospeech 
import pyaudio
import backoff

from io import StringIO, BytesIO

from text_to_speech import speech_pars_to_filename

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/agjohnst/Downloads/My First Project-492e7b29cd65.json'

cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = ['1', '2', '3', '4', '5', '6', '7', '8']
pieces = {
        'N' : 'knight',
        'R' : 'rook',
        'B' : 'bishop',
        'Q' : 'queen',
        'K' : 'king',
        'p' : 'pawn',
    }
pieces_back = { v : k for k, v in pieces.items() }
pieces_back['horse'] = 'N'
pieces_back['horsey'] = 'N'


raw_words_needed = [
    'knight',
    'rook',
    'bishop',
    'queen',
    'king',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',

    'long',

    'castles',
    'castle',

    'equals',
    
    'takes',
    'take',

    'check',
    'mate',

    'move',
    'yes',
    'no',
    'stop',
    'go',
    'ok',
    'repeat',
    'confirm',
    'playback',
] 


# voiceselectionparams args:

language_code = 'en-US'

voice_list = [
    'en-US-Standard-B',
    'en-US-Standard-C',
    'en-US-Standard-D',
    'en-US-Standard-E',
    'en-US-Wavenet-A',
    'en-US-Wavenet-B',
    'en-US-Wavenet-C',
    'en-US-Wavenet-D',
    'en-US-Wavenet-E',
    'en-US-Wavenet-F',
]

# audioconfig args
pitch_range = [-20.0, 20.0]
speaking_rate_range = [0.25, 4.0]
sample_rate_hz = 16000


# sample_variance configs
pitches_to_try = [-10.0, -5.0, 0.0, 5.0, 10.0]
speaking_rates_to_try = [0.5, 0.75, 1.0, 1.25, 1.5]

print( len(pitches_to_try) * len(speaking_rates_to_try) * len(voice_list) )

@backoff.on_exception(backoff.expo, BaseException, max_time=600)
def get_speech_audio_to_file(
                    filename, 
                    text_to_speak, 
                    voice_name          = None, 
                    pitch               = 0.0, 
                    speaking_rate       = 1.0, 
                    sample_rate_hertz   = 16000, 
                    language_code       = 'en-US'
            ):
    client = texttospeech.TextToSpeechClient()
    synth_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
                            language_code   = language_code,
                            name            = voice_name,
                            #ssml_gender     = texttospeech.enums.SsmlVoiceGender.NEUTRAL
                        )
    
    audio_config = texttospeech.types.AudioConfig(
                audio_encoding          = texttospeech.enums.AudioEncoding.MP3,
                sample_rate_hertz       = sample_rate_hertz,
                pitch                   = pitch,
            )
    response = client.synthesize_speech(synth_input, voice, audio_config)

    with open(filename, 'wb') as f:
        f.write(response.audio_content)
        f.flush()

    return True


def speech_pars_to_filename(text, voice_name, pitch, speaking_rate, sample_hertz, language_code):
    filename = 'ts_%s_te_%s_%s_%s_%s_%s.mp3'%(text.replace(' ', '_'), language_code, voice_name, int(pitch * 1000), int(speaking_rate * 1000), int(sample_hertz))
    return filename

out_dir = 'word_samples'


for text in raw_words_needed:
    for pitch in pitches_to_try:
        for speaking_rate in speaking_rates_to_try:
            for voice_name in voice_list:
                out_filename = os.path.join(out_dir, speech_pars_to_filename(text, voice_name, pitch, speaking_rate, sample_rate_hz, language_code))

                if not os.path.exists(out_filename):
                    print ("Getting sample: text='%s' voice_name=%s pitch=%s speaking_rate=%s"%(text, voice_name, pitch, speaking_rate))
                    get_speech_audio_to_file(
                            out_filename,
                            text,
                            voice_name          = voice_name,
                            pitch               = pitch,
                            speaking_rate       = speaking_rate,
                            sample_rate_hertz   = sample_rate_hz,
                            language_code       = language_code
                        )
                
     

