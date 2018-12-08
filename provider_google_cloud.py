import os
import time
import random

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import texttospeech 
import backoff

from io import StringIO, BytesIO

from text_to_speech import speech_pars_to_filename

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/agjohnst/Downloads/My First Project-492e7b29cd65.json'

PROVIDER_NAME = 'googlecloud'

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
#pitch_range = [-20.0, 20.0]
#speaking_rate_range = [0.25, 4.0]


# sample_variance configs
default_sample_rate_hz          = 16000
default_pitches_to_try          = [-10.0, -5.0, 0.0, 5.0, 10.0]
default_speaking_rates_to_try   = [0.5, 0.75, 1.0, 1.25, 1.5]

default_pitches_to_try          = [0.0] #-10.0, -5.0, 0.0, 5.0, 10.0]
default_speaking_rates_to_try   = [1.0] #0.5, 0.75, 1.0, 1.25, 1.5]

default_voices_to_try           = voice_list


#@backoff.on_exception(backoff.expo, BaseException, max_time=600)
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
    synth_input = texttospeech.types.SynthesisInput(text=text_to_speak)
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



def get_audio_files_for_phrases(
            phrases, 
            out_dir, 
            pitches                 = default_pitches_to_try, 
            rates                   = default_speaking_rates_to_try, 
            sample_rate_hz          = default_sample_rate_hz,
            voices                  = default_voices_to_try,
            randomize               = True,
        ):


    all_options = [(phrase, pitch, rate, voice) 
                        for phrase in phrases 
                        for pitch in pitches
                        for rate in rates
                        for voice in voices]
    if randomize:
        all_options = [all_options[x] for x in random.sample(range(len(all_options)), len(all_options))]


    # limits:
    # 300 requests per minute
    # 150,000 chars per minute

    limit_info = []
    limit_time = 60.0

    limit_count = 295
    limit_sum = 140000
    chars_done = 0
    
    for phrase, pitch, rate, voice in all_options:

        tcur = time.time()
        
        done = False
        while not done:
            while len(limit_info) > 0 and tcur > limit_info[0][0] + limit_time:
                limit_info.pop(0)

            
            if len(limit_info) >= limit_count or (len(limit_info) > 0 and chars_done - limit_info[0][1] >= limit_sum):
                print ("Backing off to avoid google limits: count=%s sum=%s"%(len(limit_info), chars_done - limit_info[0][1]))
                time.sleep(5)

                break
                

            done = True
        #all_phrases_reordered = [all_phrases[x] for x in random.sample(range(len(all_phrases)), len(all_phrases))]
        #for text in phrases:
        #    for pitch in pitches:
        #        for speaking_rate in rates:
        #            for voice_name in voices:
            out_filename = os.path.join(out_dir, speech_pars_to_filename(phrase, voice, pitch, rate, sample_rate_hz, language_code, PROVIDER_NAME))

            if not os.path.exists(out_filename):
                print ("Getting sample: phrase='%s' voice=%s pitch=%s rate=%s"%(phrase, voice, pitch, rate))
                get_speech_audio_to_file(
                        out_filename,
                        phrase,
                        voice_name          = voice,
                        pitch               = pitch,
                        speaking_rate       = rate,
                        sample_rate_hertz   = sample_rate_hz,
                        language_code       = language_code
                    )

                chars_done += len(phrase)
                limit_info.append((time.time(), chars_done))
                        
             

