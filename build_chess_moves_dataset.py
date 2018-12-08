
import provider_google_cloud 

from chessmoves import generate_all_possible_phrases

providers = {
    provider_google_cloud.PROVIDER_NAME : provider_google_cloud,
}


#out_dir = 'word_samples'
out_dir = 'phrase_samples'

provider_to_use = provider_google_cloud.PROVIDER_NAME


provider = providers[provider_to_use]

all_phrases = [x[1] for x in generate_all_possible_phrases(basic_mode = True)]

provider.get_audio_files_for_phrases(all_phrases, out_dir)







