# Utils/ollama.py
import config
import requests, time, json, logging, socket

def ollama_test():
    """Tests Ollama to set flag for active/inactive."""
    try:
        socket.create_connection(("localhost", 11434), timeout=1).close()
        logging.info(f"Ollama found!")
        return True
    except Exception as e:
        logging.error(f"Ollama not installed. Chat features unavailable.")
        return False

def get_all_models():
    """Fetch list of available model names from Ollama API"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            return list(set(model["name"] for model in data.get("models", [])))
        return []
    except Exception as e:
        logging.error(f"Error fetching models: {e}")
        return []

def get_loaded_models():
    """Fetch list of currently loaded models from Ollama API"""
    try:
        response = requests.get("http://localhost:11434/api/ps")
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        return []
    except Exception as e:
        logging.error(f"Error fetching loaded models: {e}")
        return []

def load_model(model):
    """Load a model into memory with a 30-minute keep-alive"""
    payload = {"model": model, "prompt": "", "stream": False, "keep_alive": "30m"}
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            start_time = time.time()
            while time.time() - start_time < 30:
                if model in get_loaded_models():
                    return True
                time.sleep(1)
            logging.info(f"Timeout loading {model}")
            return False
    except Exception as e:
        logging.error(f"Failed to load {model}: {e}")
        return False

def unload_model(model):
    """Unload a model from memory"""
    payload = {"model": model, "prompt": "", "keep_alive": 0, "stream": False}
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            start_time = time.time()
            while time.time() - start_time < 10:
                if model not in get_loaded_models():
                    return True
                time.sleep(0.5)
            logging.info(f"Timeout unloading {model}")
            return False
    except Exception as e:
        logging.error(f"Failed to unload {model}: {e}")
        return False

def chat_stream(model, messages):
    """
    Stream response from Ollama using the proper /chat endpoint.
    
    messages = list of dicts: [{"role": "user"|"assistant"|"system", "content": "..."}, ...]
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": True}
    try:
        response = requests.post(url, json=payload, stream=True, timeout=30)
        if response.status_code != 200:
            yield f"Ollama error {response.status_code}: {response.text}\n"
            return
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if chunk.get("done"):
                        break
                    yield chunk["message"]["content"]
                except json.JSONDecodeError:
                    continue
    except requests.ConnectionError:
        yield "Cannot reach Ollama — is it running?\n"
    except requests.Timeout:
        yield "Ollama timed out\n"
    except Exception as e:
        yield f"Error: {e}\n"