# Utils/ollama.py
import requests, time, json, logging, socket

def ollama_test():
    """Tests Ollama to set flag for active/inactive."""
    try:
        socket.create_connection(("localhost", 11434), timeout=1).close()
        logging.info(f"Ollama found!")
        return True
    except Exception as e:
        logging.error(f"Ollama not installed. Chat features unavailable. Error: {e}")
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
        logging.debug(f"Sent request to {model}. Response code: {response.status_code}")
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
                    logging.info(f"Unloaded {model}")
                    return True
                time.sleep(0.5)
            logging.info(f"Timeout unloading {model}")
            return False
    except Exception as e:
        logging.error(f"Failed to unload {model}: {e}")
        return False

def chat_stream(model, messages, out_q):
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
            out_q.put(f"Ollama error {response.status_code}: {response.text}\n")
            return
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if chunk.get("done"):
                        break
                    out_q.put(chunk["message"]["content"])
                except json.JSONDecodeError:
                    continue
    except requests.ConnectionError:
        out_q.put("Cannot reach Ollama — is it running?\n")
    except requests.Timeout:
        out_q.put("Ollama timed out\n")
    except Exception as e:
        out_q.put(f"Error: {e}\n")
    finally:
        out_q.put(None)

def get_model_info(model):
    """Gets detailed model information for a specific model."""
    empty_dict = {
    "architecture": "",
    "parameter_count": 0,
    "parameters": "Unknown",
    "embedding_length": "Unknown",
    "embedding_length_num": 0,
    "context_length": "Unknown",
    "context_length_num": 2048,
    "system_prompt": "No system prompt defined",
    "family": "Unknown"}
    try:   
        response = requests.post(f"http://localhost:11434/api/show", json={"name": model}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            model_info = data.get("model_info", {})
            arch = model_info.get("general.architecture", "").lower()
            param_count = model_info.get("general.parameter_count", 0)
            params_str = "Unknown"
            if param_count > 0:
                if param_count > 1e12:
                    params_str = f"{param_count / 1e12:.1f}T"
                elif param_count > 1e9:
                    params_str = f"{param_count / 1e9:.1f}B"
                elif param_count > 1e6:
                    params_str = f"{param_count / 1e6:.1f}M"
                else:
                    params_str = str(param_count)
            embed_key = f"{arch}.embedding_length" if arch else ""
            embed_str = model_info.get(embed_key, "Unknown")
            embed_num = int(embed_str) if embed_str != "Unknown" else 0
            ctx_key = f"{arch}.context_length" if arch else ""
            ctx_str = model_info.get(ctx_key, "Unknown")
            ctx_num = int(ctx_str) if ctx_str != "Unknown" else 2048
            modelfile = data.get("modelfile", "")
            system_prompt = _extract_system(modelfile)
            return {
                "architecture": arch,
                "parameter_count": param_count,
                "parameters": params_str,
                "embedding_length": embed_str,
                "embedding_length_num": embed_num,
                "context_length": ctx_str,
                "context_length_num": ctx_num,
                "system_prompt": system_prompt,
                "family": data.get("details", {}).get("family", "Unknown").capitalize()
            }
        logging.warning(f"Failed to fetch model info for {model}, status code: {response.status_code}, response: {response.text}")
        return empty_dict
    except Exception as e:
        logging.error(f"Error fetching model info for {model}: {e}")
        return empty_dict

def _extract_system(modelfile):
    """Extracts the system prompt from model details"""
    lines = modelfile.splitlines()
    system_lines = []
    in_system = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("SYSTEM"):
            in_system = True
            content = line[line.find("SYSTEM") + 6:].strip()
            if content:
                system_lines.append(content)
            continue
        if in_system:
            if stripped and stripped.split()[0].isupper() and ' ' in stripped:
                break
            system_lines.append(line.strip())
    return '\n'.join(system_lines).strip() or "No system prompt defined"