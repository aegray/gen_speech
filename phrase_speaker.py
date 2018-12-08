
import os
import time
import array
import pyaudio
import math
from pydub import AudioSegment
from pydub.utils import get_array_type

from text_to_speech import speech_pars_to_filename




def say(phrase, voice_name, pause_dur = 0.1, pitch = 1.0, speaking_rate = 1.0, sample_rate_hertz = 16000, language_code = 'en-US', clip_front = 0.1, clip_back = 0.35):

    phrase = phrase.split(' ')
    sounds = []

  
    sample_width = 2
    clip_front_in_bytes = sample_width * (math.floor(clip_front * sample_rate_hertz))
    clip_back_in_bytes = sample_width * (math.floor(clip_back * sample_rate_hertz))

    print (clip_front_in_bytes, clip_back_in_bytes)

    for i, x in enumerate(phrase):
        fname = speech_pars_to_filename(x, voice_name, pitch, speaking_rate, sample_rate_hertz, language_code)
        sound = AudioSegment.from_file(file='word_samples/' + fname)
        chan = sound.split_to_mono()[0]

        print (len(chan._data))

        use_clip_front = 0 if i == 0 else clip_front_in_bytes
        use_clip_back = 0 if i == len(phrase)-1 else clip_back_in_bytes
        sounds.append(chan._data[use_clip_front:len(chan._data)-use_clip_back])

        #data = array.array(get_array_type(chan.sample_width*8), chan._data)

        #print len(data)
        #print (type(chan._data), len(chan._data))
        #os.system("mplayer 'word_samples/%s'"%(fname))

    print ([len(x) for x in sounds])
    sound = b''.join(sounds)
    
    audio = pyaudio.PyAudio()
    stream = audio.open(
                    format      = audio.get_format_from_width(2), 
                    channels    = 1,
                    rate        = sample_rate_hertz,
                    output      = True
                )

    stream.write(sound)

    while stream.is_active():
        time.sleep(0.1)
    stream.stop_stream()
    stream.close()
    audio.terminate()

#say('knight e five', 'en-US-Wavenet-A')
say('knight f seven', 'en-US-Wavenet-A')

