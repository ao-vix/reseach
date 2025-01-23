import torch
from transformers import AutoModelForCausalLM

def load_model(model_name):
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")
    if torch.cuda.is_available():
        model = model.to("cuda")
    else:
        model = model.to("cpu")
    return model

def generate_response(model, tokenizer, prompt):
    with torch.no_grad():
        token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        token_ids = token_ids.to(model.device)
        
        output_ids = model.generate(
            token_ids,
            max_new_tokens=256,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
        
    output = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):], skip_special_tokens=True)
    return output
