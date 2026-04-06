from ollama_provider import OllamaProvider
import time

def test_ollama():
    # Initialize the provider. You can change the model_name to a model you already have installed.
    # For example: "llama3", "mistral", "phi3", etc.
    model_to_test = "gemma3:1b"
    print(f"Initializing OllamaProvider with model: {model_to_test}...")
    
    try:
        provider = OllamaProvider(model_name=model_to_test, temperature=0.7)
    except Exception as e:
        print(f"Initialization error: {e}")
        return

    system_prompt = "You are a helpful AI assistant. Please answer briefly and concisely."
    user_prompt = "Explain Machine Learning briefly in 2 sentences."

    # ==========================================
    # TEST 1: generate() function (wait for full response)
    # ==========================================
    print("\n" + "="*50)
    print("TEST 1: Running generate() function ...")
    print("="*50)
    try:
        result = provider.generate(prompt=user_prompt, system_prompt=system_prompt)
        print("\n[Response Content]:")
        print(result["content"])
        print("\n[Metrics]:")
        print(f"- Latency: {result['latency_ms']} ms")
        print(f"- Token usage: {result['usage']}")
        print(f"- Provider: {result['provider']}")
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")

    # ==========================================
    # TEST 2: stream() function (real-time response)
    # ==========================================
    print("\n" + "="*50)
    print("TEST 2: Running stream() function ...")
    print("="*50)
    try:
        print("\n[AI is responding]: ", end="", flush=True)
        # Start receiving text chunks and print them immediately
        for chunk in provider.stream(prompt=user_prompt, system_prompt=system_prompt):
            print(chunk, end="", flush=True)
            time.sleep(0.02) # Optional: Small sleep for a visual streaming effect
        print("\n\n[Stream completed]")
    except Exception as e:
        print(f"\n❌ Error in Test 2: {e}")

if __name__ == "__main__":
    test_ollama()