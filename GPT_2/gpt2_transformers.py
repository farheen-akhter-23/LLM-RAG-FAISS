import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def test_llm(model_name, test_prompt):
    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Tokenize input
    inputs = tokenizer(test_prompt, return_tensors="pt")
    
    # Generate output
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=50)
    
    # Decode output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(f"Input: {test_prompt}")
    print(f"Output: {generated_text}")
    
    # Basic tests
    assert len(generated_text) > len(test_prompt), "Model should generate additional text"
    assert test_prompt in generated_text, "Output should contain the input prompt"
    
    # Test model parameters
    assert model.config.vocab_size == len(tokenizer), "Vocab size mismatch"
    assert torch.isfinite(model.parameters().__next__()).all(), "Model has non-finite parameters"
    
    # Test attention mask
    attention_mask = inputs['attention_mask']
    assert attention_mask.shape == inputs['input_ids'].shape, "Attention mask shape mismatch"
    assert attention_mask.sum() == attention_mask.numel(), "Attention mask should be all ones for this input"

    print("All tests passed!")

# Example usage
test_llm("gpt2", "Once upon a time")