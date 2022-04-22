import os
from datetime import datetime

import psutil
import GPUtil
import platform
import tkinter
from tkinter import *

root = Tk()
root.title("DeviceCheck")
root.iconbitmap()
root.geometry('400x600')
root.resizable(False, True)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


def get_size(bytes):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}B"
        bytes /= factor


def getDiskInfo():
    diskinfo = ['Disk: ']
    for parti in psutil.disk_partitions():

        diskinfo.append('==> Device : ' + str(parti.device))
        diskinfo.append('=> Mountpoint : ' + str(parti.mountpoint))
        diskinfo.append('=> File-System-Type : ' + str(parti.fstype))
        try:
            partition_usage = psutil.disk_usage(parti.mountpoint)
        except PermissionError:
            continue
        diskinfo.append('=> Total Size : ' + str(get_size(partition_usage.total)))
        diskinfo.append('=> Used Size : ' + str(get_size(partition_usage.used)))
        diskinfo.append('=> Free Size : ' + str(get_size(partition_usage.free)))
        diskinfo.append('=> Percentage : ' + str(partition_usage.percent) + "%")

    diskinfo.append('-> Total Read: ' + str(get_size(psutil.disk_io_counters().read_bytes)))
    diskinfo.append('-> Total Write: ' + str(get_size(psutil.disk_io_counters().write_bytes)))
    diskinfo.append('')
    return diskinfo


def getGPUInfo():
    gpuinfo = ['GPU: ']
    for gpu in GPUtil.getGPUs():
        gpuinfo.append('==> Name: ' + str(gpu.name))
        gpuinfo.append('=> Load: ' + str(gpu.load + "%"))
        gpuinfo.append('=> Total Memory: ' + str(gpu.memoryTotal) + "MB")
        gpuinfo.append('=> Temperature: ' + str(gpu.temperature) + "°C")

    return gpuinfo


def getAllInfos():
    fbt = datetime.fromtimestamp(psutil.boot_time())
    infos = (
        'OS: ' + platform.uname().system,
        'Release: ' + platform.uname().release,
        'Version: ' + platform.uname().version,
        'Machine: ' + platform.uname().machine,

        '',

        'CPU: ' + platform.uname().processor,
        '-> Physical CPU-Cores: ' + str(os.cpu_count().real),
        '-> Total CPU-Cores: ' + str(psutil.cpu_count(logical=True)),
        '-> Current-frequency: ' + str(psutil.cpu_freq().current) + " GHz",
        '-> Max-frequency: ' + str(psutil.cpu_freq().max) + " GHz",
        '-> Min-frequency: ' + str(psutil.cpu_freq().min) + " GHz",
        '-> Total CPU Usage: ' + str(psutil.cpu_percent()) + "%",

        '',

        'RAM Memory: ',
        '-> Total: ' + str(get_size(psutil.virtual_memory().total)),
        '-> Used: ' + str(get_size(psutil.virtual_memory().used)),
        '-> Available: ' + str(get_size(psutil.virtual_memory().available)),
        '-> RAM Usage: ' + str(psutil.virtual_memory().percent) + "%",

        '',

        'Boot Time: ' + str(fbt.year) + '/' + str(fbt.month) + '/' + str(fbt.day) + ' ' + str(fbt.hour) + ':' +
        str(fbt.minute) + ':' + str(fbt.second),

        ''
    )

    matched = infos + tuple(getDiskInfo()) + tuple(getGPUInfo())
    return matched


infos_var = tkinter.StringVar(value=getAllInfos())

listbox = tkinter.Listbox(
    root,
    listvariable=infos_var,
    height=6,
    selectmode='extended')
listbox.grid(
    column=0,
    row=0,
    sticky='nwes'
)


def update():
    infos_var = tkinter.StringVar(value=getAllInfos())

    listbox = tkinter.Listbox(
        root,
        listvariable=infos_var,
        height=6,
        selectmode='extended')
    listbox.grid(
        column=0,
        row=0,
        sticky='nwes'
    )
    root.after(1000, update)


menubar = tkinter.Menu(root)

filemenu = tkinter.Menu(menubar)
filemenu.add_command(label="Developed by VazziDE")
filemenu.add_command(label="Twitter: https://twitter.com/vazzide")
filemenu.add_command(label="Github: https://github.com/VazziDE")

menubar.add_cascade(label="Credits", menu=filemenu)

root.config(menu=menubar)
root.after(1000, update)
root.mainloop()
