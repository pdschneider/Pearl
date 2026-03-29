# Managers/model_manager.py
from Connections.ollama import create_model_list


def parse_details(model):
    all_model_info = create_model_list()
    print(all_model_info)
    model_info = all_model_info[model]
    model_parameters = model_info["parameter_count"]

    print(f"Model: {model}")
    print(f"Parameters: {model_parameters}")

    # Determine quantization level
    quantization = model_info["quantization"]
    if "FP16" in quantization:
        quantization = 1
        ram_weight = 2.25
    elif "Q8" in quantization:
        quantization = 2
        ram_weight = 1.19
    elif "Q6" in quantization:
        quantization = 3
        ram_weight = 0.87
    elif "Q5" in quantization:
        quantization = 3
        ram_weight = 0.81
    elif "Q4" in quantization:
        quantization = 4
        ram_weight = 0.71
    elif "Q3" in quantization:
        quantization = 5
        ram_weight = 0.64
    elif "Q2" in quantization:
        quantization = 8
        ram_weight = 0.49
    elif "Q1" in quantization:
        quantization = 16
        ram_weight = 0.35
    else:
        quantization = 4
        ram_weight = 0.71
    
    # Calculate estimated RAM
    print(f"Quantization: {quantization}")
    parameters_in_billions = model_parameters / 1000000000
    estimated_ram_cost = parameters_in_billions * ram_weight + 0.7
    print(f"Estimated RAM Cost: {estimated_ram_cost}")
