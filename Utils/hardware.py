# Utils/hardware.py
import subprocess
import logging
import psutil
import platform

os_name = platform.platform()


def get_ram_info():
    """Retrieves information about total RAM & active usage."""
    try:
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        avail_ram_gb = psutil.virtual_memory().available / (1024**3)
        return {'avail_ram_gb': avail_ram_gb, 'total_ram_gb': total_ram_gb}
    except Exception as e:
        logging.warning(f"Could not retrieve RAM information: {e}.")
    if os_name.startswith("Linux"):
        try:
            with open('/proc/meminfo') as f:
                meminfo = f.read()
            total_ram_gb = int(meminfo.split(
                'MemTotal:')[1].split('kB')[0].strip()) / (1024**2)
            avail_ram_gb = int(meminfo.split(
                'MemAvailable:')[1].split('kB')[0].strip()) / (1024**2)
            return {'avail_ram_gb': avail_ram_gb, 'total_ram_gb': total_ram_gb}
        except Exception as e:
            logging.warning(
                f"Could not retrieve RAM information from /proc/meminfo: {e}.")
            return {'avail_ram_gb': None, 'total_ram_gb': None}
    else:
        return {'avail_ram_gb': None, 'total_ram_gb': None}


def get_cpu_info():
    """Retrieves the number of CPU threads."""
    try:
        cpu_threads = psutil.cpu_count(logical=True)
        return {'cpu_threads': cpu_threads}
    except Exception as e:
        logging.warning(f"Unable to retrieve CPU thread count: {e}")
    if os_name.startswith("Linux"):
        try:
            with open('/proc/cpuinfo') as f:
                cpuinfo = f.read()
            cpu_threads = cpuinfo.count('processor')
            return {'cpu_threads': cpu_threads}
        except Exception as e:
            logging.warning(
                f"Unable to retrieve CPU thread count from /proc/cpuinfo: {e}")
            return {'cpu_threads': None}
    else:
        return {'cpu_threads': None}


def cpu_temp_info():
    """Retrieves CPU temperature."""
    if os_name.startswith("Linux"):
        try:
                temp_output = psutil.sensors_temperatures()
                # AMD:
                if 'k10temp' in temp_output:
                    return {'cpu_temp_c': temp_output['k10temp'][0].current}
                # Intel:
                elif 'coretemp' in temp_output:
                    for entry in temp_output['coretemp']:
                        if 'Package' in entry.label or 'Core 0' in entry.label:
                            return {'cpu_temp_c': entry.current}
                    return {'cpu_temp_c': temp_output['coretemp'][0].current}
                else:
                    logging.warning(f"Initial CPU temp failed. Falling back to sensors command...")
        except Exception as e:
            logging.warning(f"Unable to retrieve CPU temperature data: {e}")
            logging.warning(f"Falling back to sensors command...")
    if os_name.startswith("Linux"):
        try:
            # Fallback: Uses sensors bash command to pull data from
            # sensors internal Linux file for finding CPU temperature
            sensors_output = subprocess.check_output(
                ['sensors']).decode('utf-8')
            cpu_temp_c = None
            # Iterates between each line of temp_output
            for line in sensors_output.split('\n'):
                # Checks for the words Core or Tdie in each line
                if 'Core' in line or 'Tdie' in line or 'Tctl' in line:
                    # Saves temp as a float, stripping non-numerical characters
                    cpu_temp_c = float(
                        line.split(':')[1].split('°C')[0].strip('+'))
            return {'cpu_temp_c': cpu_temp_c} if cpu_temp_c is not None else {}
        except Exception as e:
            logging.warning(f"Unable to retrieve CPU temperature: {e}")
            return {'cpu_temp_c': None}
    else:
        return {'cpu_temp_c': None}


def get_l3_cache():
    """Fetches the size of the CPU's l3 cache."""
    if os_name.startswith("Linux"):
        try:
            output = subprocess.check_output(
                "lscpu | grep L3", shell=True).decode('utf-8').strip()
            parts = output.split()
            l3_size_str = parts[2]  # '64'
            l3_unit = parts[3]  # 'MiB'
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
    elif os_name.startswith("Windows"):
        try:
            # Use PowerShell to query Win32_Processor.L3CacheSize (in KB)
            # subprocess.call PowerShell with minimal flags
            ps_cmd = (
                "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "
                "\"(Get-CimInstance -ClassName Win32_Processor).L3CacheSize\""
            )
            output = subprocess.check_output(ps_cmd, shell=True, text=True, timeout=5).strip()

            if output and output.isdigit():
                size_kb = int(output)
                size_mb = size_kb / 1024.0  # KB → MiB
                if size_mb > 0:
                    logging.debug(f"PowerShell L3 cache size: {size_mb:.1f} MiB")
                    return {'l3_size': round(size_mb)}
                else:
                    logging.debug("L3CacheSize reported as 0 KB")
        except Exception as e:
            logging.warning(f"Failed PowerShell L3 cache query: {e}")
    else:
        return {'l3_size': 8}


def get_gpu_info():
    has_llm_gpu = False
    gpu_vram_gb = 0
    gpu_type = "None"

    # Check for NVIDIA GPU
    try:
        nvidia_test = subprocess.run('nvidia-smi', shell=True, capture_output=True, timeout=4)
        if nvidia_test.returncode == 0:
            nvidia_output = subprocess.check_output(
                ['nvidia-smi',
                '--query-gpu=memory.total',
                '--format=csv,noheader,nounits']).decode('utf-8').strip()
            if nvidia_output:
                gpu_vram_gb = int(nvidia_output.split('\n')[0]) / 1024
                has_llm_gpu = True
                gpu_type = "NVIDIA"
                return {'has_llm_gpu': has_llm_gpu, 'gpu_vram_gb': gpu_vram_gb, 'gpu_type': gpu_type}
    except Exception as e:
        logging.warning(f"Unable to retrieve NVIDIA GPU information: {e}.")
        pass

    # Check for AMD GPU with ROCm
    if not has_llm_gpu:
        try:
            amd_test = subprocess.run('rocm-smi', shell=True, capture_output=True, timeout=4)
            if amd_test.returncode == 0:
                # If successful, check for errors
                amd_test = subprocess.run('rocm-smi | grep ERROR', shell=True, capture_output=True, timeout=4)
                if amd_test:
                    return {'has_llm_gpu': has_llm_gpu, 'gpu_vram_gb': gpu_vram_gb, 'gpu_type': gpu_type}
                amd_test = subprocess.run('rocm-smi | grep Not supported', shell=True, capture_output=True, timeout=4)
                if amd_test:
                    return {'has_llm_gpu': has_llm_gpu, 'gpu_vram_gb': gpu_vram_gb, 'gpu_type': gpu_type}
                amd_test = subprocess.run('rocm-smi | grep unsupported', shell=True, capture_output=True, timeout=4)
                if amd_test:
                    return {'has_llm_gpu': has_llm_gpu, 'gpu_vram_gb': gpu_vram_gb, 'gpu_type': gpu_type}

                # If still successful, query for more detailed info
                rocm_output = subprocess.check_output(
                    ['rocm-smi', '--showmeminfo', 'vram']).decode('utf-8')
                if 'VRAM Total Memory' in rocm_output:
                    vram_line = [line for line in rocm_output.split('\n') if 'VRAM Total Memory' in line][0]
                    gpu_vram_gb = int(vram_line.split()[-2]) / (1024**3)
                    has_llm_gpu = True
                    gpu_type = "AMD with ROCm"
        except Exception as e:
            logging.warning(f"Unable to retrieve AMD GPU information: {e}.")
            pass
    return {'has_llm_gpu': has_llm_gpu, 'gpu_vram_gb': gpu_vram_gb, 'gpu_type': gpu_type}


def get_disk_space():
    """Collects disk usage statistics."""
    try:
        disk = psutil.disk_usage('/')
        total = int(disk.total / (1024**3))
        used = int(disk.used / (1024**3))
        free = int(disk.free / (1024**3))
        percent = disk.percent
        return {'total_disk': total, 'used_disk': used, 'free_disk': free, 'percent_disk': percent}
    except Exception as e:
        logging.error(f"Could not calculate disk space due to {e}")


def get_hardware_stats():
    """Collect system hardware stats (RAM, CPU, GPU)."""
    ram = get_ram_info()
    cpu = get_cpu_info()
    cput = cpu_temp_info()
    l3c = get_l3_cache()
    gpu = get_gpu_info()
    disk = get_disk_space()

    stats = {**ram, **cpu, **cput, **l3c, **gpu, **disk}

    try:
        logging.info("\nDetected Hardware:")
        logging.info(f"  - OS: {os_name}")
        logging.info(f"  - RAM: {stats['avail_ram_gb']:.1f}GB available / {stats['total_ram_gb']:.1f}GB total")
        logging.info(f"  - CPU Threads: {stats['cpu_threads']}")
        logging.info(f"  - CPU Temperature: {stats['cpu_temp_c']}°C")
        try:
            logging.info(f"  - L3 Cache Size: {stats['l3_size']}MiB")
            logging.info(f"  - DISK: {stats['free_disk']}GB free / {stats['total_disk']} total / {stats['used_disk']} used")
        except:
            logging.info(f"Unable to parse L3 cache")
        logging.info(f"  - LLM-capable GPU: {'Yes' if stats['has_llm_gpu'] else 'No'} ({stats['gpu_type']}, {stats['gpu_vram_gb']:.1f}GB VRAM)\n")

    except:
        pass

    return stats
