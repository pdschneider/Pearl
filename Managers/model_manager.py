from Utils.hardware import get_hardware_stats

def select_optimal_variant(base):
    """Select best model variant based on hardware"""
    stats = get_hardware_stats()
    if 'llama' in base.lower():
        if stats['has_llm_gpu'] and stats['gpu_vram_gb'] >= 8:
            return "llama3:latest"
        elif stats['avail_ram_gb'] >= 8 and stats['cpu_threads'] >= 16:
            return "llama3.2:3b-instruct-q8_0"
        else:
            return "llama3.2:latest"
    return f"{base}:latest"