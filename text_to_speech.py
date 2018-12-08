
available_voices = [
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

all_raw_words = [
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

def speech_pars_to_filename(text, voice_name, pitch, speaking_rate, sample_hertz, language_code):
    filename = 'ts_%s_te_%s_%s_%s_%s_%s.mp3'%(text.replace(' ', '_'), language_code, voice_name, int(pitch * 1000), int(speaking_rate * 1000), int(sample_hertz))
    return filename

def speech_pars_from_filename(filename):

    ext = '.'.join(filename.split('.')[1:])

    parts = filename[:-(len(ext)+1)].split('_')

    
    if parts[0] != 'ts' or not 'te' in parts:
        raise ValueError("invalid filename")

    end_text = parts.index('te')
    return dict(
            text                = ' '.join(parts[1:end_text]),
            language_code       = parts[end_text+1],
            voice_name          = parts[end_text+2],
            pitch               = int(parts[end_text+3]) / 1000.0,
            speaking_rate       = int(parts[end_text+4]) / 1000.0,
            sample_hertz        = int(parts[end_text+5])
        )


    #filename = 'ts_%s_te_%s_%s_%s_%s_%s.mp3'%(text.replace(' ', '_'), language_code, voice_name, int(pitch * 1000), int(speaking_rate * 1000), int(sample_hertz))
    #return filename
