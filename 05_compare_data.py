import os
import argparse
from tool import fileTool as FT
from tool.mpTool import TaskManager
from tqdm import tqdm
from pathlib import Path


def run_command(cmd):
    print(cmd)
    os.system(cmd)


def diff_bit_log(file, dst_file, log_file):
    f1 = open(file, 'rb')
    f2 = open(dst_file, 'rb')
    log = open(log_file, 'w')

    offset = 0
    masks = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
    for c1, c2 in zip(f1.read(), f2.read()):
        for i, m in enumerate(masks):
            if((c1 & m) ^ (c2 & m)):
                log.write(f'{offset+i}\n')
        offset += 8

    f1.close()
    f2.close()
    log.close()


def compare_data(src, dst, cpp):
    files = FT.getAllFiles(src)
    pbar = tqdm(total=len(files))
    for file in files:
        dst_file = Path(dst) / Path(file).name
        log_file = Path(dst) / Path('log_' + Path(file).name)
        os.system(f'touch {log_file}')
        if cpp:
            cmd = f'cpp/diff_bit_log {file} {dst_file} {log_file}'
            run_command(cmd)
        else:
            diff_bit_log(file, dst_file, log_file)
        pbar.update(1)
    pbar.close()


def compare_data_mp(src, dst, cpp):
    files = FT.getAllFiles(src)
    tm = TaskManager(processes=8, queue_size=4, callback=None)
    pbar = tqdm(total=len(files))
    for file in files:
        dst_file = Path(dst) / Path(file).name
        log_file = Path(dst) / Path('log_' + Path(file).name)
        os.system(f'touch {log_file}')
        if cpp:
            cmd = f'cpp/diff_bit_log {file} {dst_file} {log_file}'
            tm.new_task(run_command, cmd)
        else:
            tm.new_task(diff_bit_log, file, dst_file, log_file)
        pbar.update(1)
    pbar.close()
    tm.close()


def compute_uber(src, dst):
    total = 0
    files = FT.getAllFiles(src)
    for file in files:
        total += int(os.path.getsize(file)) * 8

    error_total = 0
    dst_files = FT.getAllFiles(dst)
    log_files = [file for file in dst_files if file.count('log')]
    for log_file in log_files:
        log = open(log_file)
        error_total += len(log.readlines())

    uber_file = Path(dst) / Path('0_UBER')
    os.system(f'touch {uber_file}')
    uber = open(uber_file, 'w')
    uber.write(f'error_total:{error_total:e} total:{total:e} UBER:{float(error_total)/total:e}')


def clear_data(src, dst):
    files = FT.getAllFiles(src)
    for i, file in enumerate(files):
        dst_file = Path(dst) / Path(file).name
        if i == 0:
            cmd = f'sudo -S rm {dst_file}'
        else:
            cmd = f'sudo -S rm {dst_file} < password'
        run_command(cmd)

def check_data(src):
    files = FT.getAllFiles(src)
    files = [file for file in files if file.count('writers')]
    log_file = Path(src) / Path('log')
    if os.path.exists(log_file):
        os.system(f'rm {log_file}')
    os.system(f'touch {log_file}')
    pbar = tqdm(total=len(files))
    for file in files:
        cmd = f'cpp/check_data {file} {log_file}'
        run_command(cmd)
        pbar.update(1)
    pbar.close()


def write_data(src, dst):
    FT.mkPath(src)
    FT.mkPath(dst)

    file = f'{src}/a'
    os.system(f'touch {file}')
    f = open(file, 'wb')
    for i in range(1024 * 1024):
        f.write(bytes([15]))

    file = f'{dst}/a'
    os.system(f'touch {file}')
    f = open(file, 'wb')
    for i in range(1024 * 1024):
        f.write(bytes([255]))


pe_cycle = 50
retention = 5


def intel_670p():
    type = 'SSD_Intel_670P'
    capacity = 384
    device = '/dev/nvme1n1'

    src = 'data/384G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    compare_data(src, dst, cpp=True)
    compute_uber(src, dst)
    clear_data(src, dst)


def kingston_nv1():
    type = 'SSD_Kingston_NV1'
    capacity = 768
    device = '/dev/nvme3n1'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    compare_data(src, dst, cpp=True)
    compute_uber(src, dst)
    clear_data(src, dst)


def seagate_q5():
    type = 'SSD_Seagate_Q5'
    capacity = 384
    device = '/dev/nvme2n1'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    compare_data(src, dst, cpp=True)
    compute_uber(src, dst)
    clear_data(src, dst)


def samsung_870qvo():
    type = 'SSD_SAMSUNG_870QVO'
    capacity = 768
    device = '/dev/sdb'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    compare_data(src, dst, cpp=True)
    compute_uber(src, dst)
    clear_data(src, dst)


def sandisk_redgrey():
    type = 'TF_SanDisk_RedGrey'
    capacity = 96
    device = '/dev/sdd'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    compare_data(src, dst, cpp=True)
    compute_uber(src, dst)
    clear_data(src, dst)


def netac_u185():
    type = 'USB_Netac_U185'
    capacity = 96
    device = '/dev/sdc'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    compare_data(src, dst, cpp=True)
    compute_uber(src, dst)
    clear_data(src, dst)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('choice', type=int)
    args = parser.parse_args()

    if args.choice == 0:
        print('choose intel')
        intel_670p()
    elif args.choice == 1:
        print('choose kingston')
        kingston_nv1()
    elif args.choice == 2:
        print('choose seagate')
        seagate_q5()
    elif args.choice == 3:
        print('choose samsung')
        samsung_870qvo()
    elif args.choice == 4:
        print('choose sandisk')
        sandisk_redgrey()
    elif args.choice == 5:
        print('choose netac')
        netac_u185()