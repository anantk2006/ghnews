from transformers import AutoModel, AutoTokenizer

checkpoint = "codesage-small-v2"
device = "cpu"  # for GPU usage or "cpu" for CPU usage

# Note: CodeSage requires adding eos token at the end of each tokenized sequence 

tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True, add_eos_token=True)

model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

inputs = tokenizer.encode("def print_hello_world():\tprint('Hello World!')", return_tensors="pt").to(device)
print(inputs)
embedding = model(inputs)[0]
print(embedding.shape)
