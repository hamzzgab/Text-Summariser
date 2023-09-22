import torch.cuda
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import pipeline
from colorama import Fore, Style
import textwrap

from data import example_text

# PICK A MODEL
#   find models on HuggingFace
MODEL_NAME = "google/pegasus-xsum"
DEVICE = 'mps' if torch.backends.mps.is_available() else 'cpu'


print(f"MODEL NAME: {MODEL_NAME}")
print(f"DEVICE: {DEVICE}")

# LOAD PRETRAINED TOKENIZER
try:
    PEGASUS_TOKENIZER = PegasusTokenizer.from_pretrained(MODEL_NAME)
except RuntimeError as error:
    print(Fore.RED + f'Something went wrong, in \'LOADING PEGASUS TOKENIZER\': \n\t{textwrap.fill(str(error), width=100)}'
          + Style.RESET_ALL)
    PEGASUS_TOKENIZER = None
else:
    print(Fore.GREEN + f"PEGASUS_TOKENIZER LOADED" + Style.RESET_ALL)

# DEFINE PEGASUS MODEL
PEGASUS_MODEL = PegasusForConditionalGeneration.from_pretrained(MODEL_NAME)

# CREATE TOKENS
#   pt -> pytorch
tokens = PEGASUS_TOKENIZER(example_text, truncation=True,
                           padding="longest", return_tensors="pt")

# SUMMARISE TEXT
encoded_summary = PEGASUS_MODEL.generate(**tokens)

# DECODE SUMMARISED TEXT
decoded_summary = PEGASUS_TOKENIZER.decode(encoded_summary[0],
                                           skip_special_tokens=True)

print(Fore.GREEN + f"TEXT SUMMARISED" + Style.RESET_ALL)
print(f'\t{textwrap.fill(decoded_summary, width=100)}')

print("|PIPELINE|"*7)

# DEFINE SUMMARIZATION PIPELINE
try:
    summariser = pipeline("summarization")
                          # model_name=MODEL_NAME,
                          # tokenizer=PEGASUS_TOKENIZER, framework="pt")
except RuntimeError as error:
    print(Fore.RED + f'Something went wrong, in the \'SUMMARISER PIPELINE\': \n\t{textwrap.fill(str(error), width=100)}'
          + Style.RESET_ALL)

    summariser = None
else:
    print(Fore.GREEN + f"SUMMARISER PIPELINE CREATED" + Style.RESET_ALL)


summary = summariser(example_text, min_length=30, max_length=150,
                     do_sample=False, num_beams=4, length_penalty=2.0)
print(Fore.GREEN + f"TEXT SUMMARISED" + Style.RESET_ALL)
print(f'\t{textwrap.fill(summary[0]["summary_text"], width=100)}')
