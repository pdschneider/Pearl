# Utils/hardware.py
import subprocess, logging, psutil
from themes import os_name

def get_ram_info():
    """Retrieves information about total RAM & active usage"""
    try:
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        avail_ram_gb = psutil.virtual_memory().available / (1024**3)
        return {'avail_ram_gb': avail_ram_gb, 'total_ram_gb': total_ram_gb}
    except Exception as e:
        logging.warning(f"Could not retrieve RAM information: {e}.")
    if os_name == "Linux":
        try:
            with open('/proc/meminfo') as f:
                meminfo = f.read()
            total_ram_gb = int(meminfo.split('MemTotal:')[1].split('kB')[0].strip()) / (1024**2)
            avail_ram_gb = int(meminfo.split('MemAvailable:')[1].split('kB')[0].strip()) / (1024**2)
            return {'avail_ram_gb': avail_ram_gb, 'total_ram_gb': total_ram_gb,}
        except Exception as e:
            logging.warning(f"Could not retrieve RAM information from /proc/meminfo: {e}.")
            return {'avail_ram_gb': None, 'total_ram_gb': None}
    else:
        return {'avail_ram_gb': None, 'total_ram_gb': None}

def get_cpu_info():
    """Retrieves the number of CPU threads"""
    try:
        cpu_threads = psutil.cpu_count(logical=True)
        return {'cpu_threads': cpu_threads}
    except Exception as e:
        logging.warning(f"Unable to retrieve CPU thread count: {e}")
    if os_name == "Linux":
        try:
            with open('/proc/cpuinfo') as f:
                cpuinfo = f.read()
            cpu_threads = cpuinfo.count('processor')
            return {'cpu_threads': cpu_threads}
        except Exception as e:
            logging.warning(f"Unable to retrieve CPU thread count from /proc/cpuinfo: {e}")
            return {'cpu_threads': None}
    else:
        return {'cpu_threads': None}

def cpu_temp_info():
    """Retrieves CPU temperature"""
    try:
        temp_output = psutil.sensors_temperatures()
        # AMD:
        if 'k10temp' in temp_output:
            return {'cpu_temp_c': temp_output['k10temp'][0].current}
        # Intel:
        if 'coretemp' in temp_output:
            for entry in temp_output['coretemp']:
                if 'Package' in entry.label or 'Core 0' in entry.label:
                    return {'cpu_temp_c': entry.current}
            return {'cpu_temp_c': temp_output['coretemp'][0].current}
    except Exception as e:
        logging.warning(f"Unable to retrieve CPU temperature data: {e}")
    if os_name == "Linux":
        try:
            sensors_output = subprocess.check_output(['sensors']).decode('utf-8') # Uses sensors bash command to pull data from sensors internal Linux file for finding CPU temperature
            cpu_temp_c = None
            for line in sensors_output.split('\n'): # Iterates between each line of temp_output
                if 'Core' in line or 'Tdie' in line or 'Tctl' in line: # Checks for the words Core or Tdie in each line (Tdie is a critical overheating condition)
                    cpu_temp_c = float(line.split(':')[1].split('°C')[0].strip('+')) # Saves temp as a float, stripping non-numerical characters
            return {'cpu_temp_c': cpu_temp_c} if cpu_temp_c is not None else {}
        except Exception as e:
            logging.warning(f"Unable to retrieve CPU temperature: {e}")
            return {'cpu_temp_c': None}
    else:
        return {'cpu_temp_c': None}
    
# Currently not functional - needs work
def get_l3_cache():
    """Fetches the size of the CPU's l3 cache"""
    try:
        output = subprocess.check_output("lscpu", shell=True).decode('utf-8').strip()
        parts = output.split()
        l3_size_str = parts[1]  # e.g., '64'
        l3_unit = parts[2]  # e.g., 'MiB'
        l3_size = float(l3_size_str)
        if l3_unit == 'KiB':
            l3_size_mb = l3_size / 1024
        elif l3_unit == 'MiB':
            l3_size_mb = l3_size
        elif l3_unit == 'GiB':
            l3_size_mb = l3_size * 1024
        else:
            l3_size_mb = 32  # Fallback
        logging.debug(f"Parsed L3 cache size: {l3_size_mb:.1f} MiB")
        return {'l3_size': l3_size_mb}
    except Exception as e:
        logging.warning(f"Failed to parse L3 cache: {e}, using fallback 8 MiB")
        return {'l3_size': 8}

def get_gpu_info():
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
    except Exception as e:
        logging.warning(f"Unable to retrieve NVIDIA GPU information: {e}.")
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
        except Exception as e:
            logging.warning(f"Unable to retrieve AMD GPU information: {e}.")
            pass
    return {'has_llm_gpu': has_llm_gpu, 'gpu_vram_gb': gpu_vram_gb, 'gpu_type': gpu_type}

def get_hardware_stats():
    """Collect system hardware stats (RAM, CPU, GPU)"""
    ram = get_ram_info()
    cpu = get_cpu_info()
    cput = cpu_temp_info()
    l3c = get_l3_cache()
    gpu = get_gpu_info()
    
    stats = {**ram, **cpu, **cput, **l3c, **gpu}
    
    try:
        logging.info("Detected Hardware:")
        logging.info(f"  - RAM: {stats['avail_ram_gb']:.1f}GB available / {stats['total_ram_gb']:.1f}GB total")
        logging.info(f"  - CPU Threads: {stats['cpu_threads']}")
        logging.info(f"  - CPU Temperature: {stats['cpu_temp_c']}°C")
        # logging.info(f"  - L3 Cache Size: {stats['l3_size']}")
        logging.info(f"  - LLM-capable GPU: {'Yes' if stats['has_llm_gpu'] else 'No'} ({stats['gpu_type']}, {stats['gpu_vram_gb']:.1f}GB VRAM)")
    except:
        pass

    return stats