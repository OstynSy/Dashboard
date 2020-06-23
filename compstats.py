import psutil
import GPUtil

def get_gpu_stats():
    gpus = GPUtil.getGPUs()
    list_gpus = []
    list = []

    for gpu in gpus:
        # name of GPU
        gpu_name = gpu.name
        # get % percentage of GPU usage of that GPU
        gpu_load = gpu.load * 100
        # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} °C"
        list = [gpu_name, gpu_load, gpu_temperature]
        list_gpus.append(list)
        return list_gpus

def get_disk_stats():
    conversion = 1024 ** 3
    disk_c = psutil.disk_usage('C:\\')
    disk_c_gb = [int(disk_c.total / conversion), int(disk_c.used / conversion), int(disk_c.free / conversion)]

    disk_g = psutil.disk_usage('G:\\')
    disk_g_gb = [int(disk_g.total / conversion), int(disk_g.used / conversion), int(disk_g.free / conversion)]

    drive_data = [disk_c_gb,disk_g_gb]
    return drive_data

def get_cpu_ram_stats():
    list = [psutil.cpu_percent(), psutil.virtual_memory().percent]
    return list


