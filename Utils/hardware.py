# Utils/hardware.py
import subprocess

def get_hardware_stats():
    """Collect system hardware stats (RAM, CPU, GPU)"""
    with open('/proc/meminfo') as f:
        meminfo = f.read()
    total_ram_gb = int(meminfo.split('MemTotal:')[1].split('kB')[0].strip()) / (1024**2)
    avail_ram_gb = int(meminfo.split('MemAvailable:')[1].split('kB')[0].strip()) / (1024**2)
    
    with open('/proc/cpuinfo') as f:
        cpuinfo = f.read()
    cpu_threads = cpuinfo.count('processor')
    
    has_llm_gpu = False
    gpu_vram_gb = 0
    gpu_type = "None"
    
    # Check for NVIDIA GPU
    try:
        nvidia_output = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits']).decode('utf-8').strip()
        if nvidia_output:
            gpu_vram_gb = int(nvidia_output.split('\n')[0]) / 1024
            has_llm_gpu = True
            gpu_type = "NVIDIA"
    except:
        pass
    
    # Check for AMD GPU with ROCm
    if not has_llm_gpu:
        try:
            rocm_output = subprocess.check_output(['rocm-smi', '--showmeminfo', 'vram']).decode('utf-8')
            if 'VRAM Total Memory' in rocm_output:
                vram_line = [line for line in rocm_output.split('\n') if 'VRAM Total Memory' in line][0]
                gpu_vram_gb = int(vram_line.split()[-2]) / (1024**3)
                has_llm_gpu = True
                gpu_type = "AMD with ROCm"
        except:
            pass
    
    return {
        'avail_ram_gb': avail_ram_gb,
        'total_ram_gb': total_ram_gb,
        'cpu_threads': cpu_threads,
        'has_llm_gpu': has_llm_gpu,
        'gpu_vram_gb': gpu_vram_gb,
        'gpu_type': gpu_type
    }

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

def initialize_hardware():
    """Detect hardware and select initial model"""
    stats = get_hardware_stats()
    if stats['has_llm_gpu'] and stats['gpu_vram_gb'] >= 8:
        model_name = "Llama 3"
        model = "llama3:latest"
    elif stats['avail_ram_gb'] >= 16 and stats['cpu_threads'] >= 16:
        model_name = "Llama 3.2 q8"
        model = "llama3.2:3b-instruct-q8_0"
    else:
        model_name = "Llama 3.2 latest"
        model = "llama3.2:latest"
    print("Detected Hardware:")
    print(f"  - RAM: {stats['avail_ram_gb']:.1f}GB available / {stats['total_ram_gb']:.1f}GB total")
    print(f"  - CPU Threads: {stats['cpu_threads']}")
    print(f"  - LLM-capable GPU: {'Yes' if stats['has_llm_gpu'] else 'No'} ({stats['gpu_type']}, {stats['gpu_vram_gb']:.1f}GB VRAM)")
    return model_name, model