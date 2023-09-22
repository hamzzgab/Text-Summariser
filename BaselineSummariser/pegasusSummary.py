from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from data import example_text

# PICK A MODEL
model_name = "google/pegasus-xsum"
#   find models on HuggingFace

# LOAD PRETRAINED TOKENIZER
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

# DEFINE PEGASUS MODEL
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)

# CREATE TOKENS
tokens = pegasus_tokenizer(example_text, truncation=True,
                           padding="longest", return_tensors="pt")
