

cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = ['1', '2', '3', '4', '5', '6', '7', '8']

rows_as_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']

pieces_to_code = {
    'knight'    : 'N',
    'rook'      : 'R',
    'bishop'    : 'B',
    'queen'     : 'Q',
    'king'      : 'K',
}

pieces = list(pieces_to_code.keys())
#piece_map.values()
#pieces_back = { v : k for k, v in pieces.items() }
#pieces_back['horse'] = 'N'
#pieces_back['horsey'] = 'N'

#raw_words_needed = pieces.values() + cols + rows
#pieces_back.keys() + cols

modifier_words = [
    'long',
    'castle', 
    #'castles', 
    'take',
    #'takes',
    'equals',
]

attack_words = [
    'check',
    'mate',
]

additional_commands = [
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
additional_phrase_commands = ['no playback', 'no confirm']

raw_words_needed = pieces + cols + rows + modifier_words + attack_words + additional_commands + ['no playback', 'no confirm']

def get_all_possible_words(): return raw_words_needed


#### format of phrases:
## piece moves
# piece col row [check | mate]
# piece takes col row [check | mate]
# piece col [take] col row [check | mate]  # constraint: we can cut down the number of these by possible moves for each piece
# piece row [take] col row [check | mate] # constraint: same as previous - cut down number of these
# ### probably one more full square disambiguation but I'm not worrying about it for now

## pawn moves
# col row_2_7 [check | mate] 
# col takes colB row_2_7 [check | mate] # constraint: colB must be one off col
# col row_1_8 equals piece [check | mate]
# col takes colB row_1_8 equals piece [check | mate] # constraint: colB must be one off col


# specials:
# castle [check | mate]
# long castle [check | mate]

# additional voice phrases

# optional but I may leave out:
# piece takes piece
# col takes col
# col row_1_8 piece [check | mate]
# col takes colB row_1_8 piece [check | mate]

# holy shit this will be big
def generate_all_possible_phrases(basic_mode = False):
    # additionally, for now I'm leaving out check + mate as its spurious
    phrases = additional_commands[:] + additional_phrase_commands[:]

    phrases.extend(['castle', 'long castle'])


    ## piece moves

    # piece col row
    # piece takes col row [check | mate]
    for icol, col in enumerate(cols):
        for irow, row in enumerate(rows):
            for piece in pieces:
                phrases.append(('%s%s%s'%(pieces_to_code[piece], col, row), '%s %s %s'%(piece, col, row)))
                phrases.append(('%sx%s%s'%(pieces_to_code[piece], col, row), '%s take %s %s'%(piece, col, row)))

            # figure out what duplicate pieces could get to this square

            # knight from col
            if not basic_mode:
                for i in [-2, -1, 1, 2]:
                    if icol + i >= 0 and icol + i < len(cols): 
                        phrases.append(('N%s%s%s'%(cols[icol+i], col, row), 'knight %s %s %s'%(cols[icol+i], col, row)))
                        phrases.append(('N%sx%s%s'%(cols[icol+i], col, row), 'knight %s take %s %s'%(cols[icol+i], col, row)))
                    if irow + i >= 0 and irow + i < len(rows):
                        phrases.append(('N%s%s%s'%(rows[irow+i], col, row), 'knight %s %s %s'%(rows[irow+i], col, row)))
                        phrases.append(('N%sx%s%s'%(rows[irow+i], col, row), 'knight %s take %s %s'%(rows[irow+i], col, row)))
            
            # rook moves
            if not basic_mode:
                for piece in ['bishop', 'rook', 'queen']:
                    for fcol in cols:
                        phrases.append(('%s%s%s%s'%(pieces_to_code[piece], fcol, col, row), '%s %s %s %s'%(piece, fcol, col, row)))
                        phrases.append(('%s%sx%s%s'%(pieces_to_code[piece], fcol, col, row), '%s %s take %s %s'%(piece, fcol, col, row)))
                    for frow in rows:
                        phrases.append(('%s%s%s%s'%(pieces_to_code[piece], frow, col, row), '%s %s %s %s'%(piece, frow, col, row)))
                        phrases.append(('%s%sx%s%s'%(pieces_to_code[piece], frow, col, row), '%s %s take %s %s'%(piece, frow, col, row)))


            # pawn moves

            if irow in [0, 7]:
                promotion_pieces = ['queen'] if basic_mode else ['queen', 'bishop', 'rook', 'knight']
                # promotion pawn moves
                for promotion_piece in promotion_pieces:
                    phrases.append(('%s%s=%s'%(col, row, pieces_to_code[promotion_piece]), '%s %s equals %s'%(col, row, promotion_piece)))
                    if icol > 0: phrases.append(('%sx%s%s=%s'%(cols[icol-1], col, row, pieces_to_code[promotion_piece]), '%s take %s %s equals %s'%(cols[icol-1], col, row, promotion_piece)))
                    if icol < 7: phrases.append(('%sx%s%s=%s'%(cols[icol+1], col, row, pieces_to_code[promotion_piece]), '%s take %s %s equals %s'%(cols[icol+1], col, row, promotion_piece)))
            else:
                # normal pawn moves 
                phrases.append(('%s%s'%(col, row), '%s %s'%(col, row)))
                if icol > 0: phrases.append(('%sx%s%s'%(cols[icol-1], col, row), '%s take %s %s'%(cols[icol-1], col, row)))
                if icol < 7: phrases.append(('%sx%s%s'%(cols[icol+1], col, row), '%s take %s %s'%(cols[icol+1], col, row)))
                
       
#    print ("Have %s phrases total"%(len(phrases)))
#    total_chars = sum([len(x[1]) for x in phrases])
#    print ("Have %s total characters in all phrases"%(total_chars))
#
#    num_voices_std = 4
#    pricing_std = 4.0 / 1000000.0
#
#    num_voices_wave = 6
#    pricing_wave = 16.0 / 1000000.0
#
#    num_rates = 1
#    num_pitches = 1
#
#    pricing = total_chars * (num_rates + num_pitches) * (num_voices_std * pricing_std + num_voices_wave * pricing_wave)
#    print ("Pricing: ", pricing)
#

    return phrases
#print (len(phrases))
            

#for x in generate_all_possible_phrases():
#    #pass
#    print x












#
#raw_words_needed = [
#    'knight',
#    'rook',
#    'bishop',
#    'queen',
#    'king',
#    'a',
#    'b',
#    'c',
#    'd',
#    'e',
#    'f',
#    'g',
#    'h',
#    
#    'one',
#    'two',
#    'three',
#    'four',
#    'five',
#    'six',
#    'seven',
#    'eight',
#
#    'long',
#
#    'castles',
#    'castle',
#
#    'equals',
#    
#    'takes',
#    'take',
#
#    'check',
#    'mate',
#
#    'move',
#    'yes',
#    'no',
#    'stop',
#    'go',
#    'ok',
#    'repeat',
#    'confirm',
#    'playback',
#] 
#
