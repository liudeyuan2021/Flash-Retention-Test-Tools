import os
import argparse
from tool import fileTool as FT
from tool.mpTool import TaskManager
from tqdm import tqdm
from pathlib import Path


def run_command(cmd):
    print(cmd)
    os.system(cmd)


def load_data(src, dst, device):
    cnt = 0
    FT.mkPath(dst)
    files = FT.getAllFiles(src)
    pbar = tqdm(total=len(files))
    for file in files:
        dst_file = Path(dst) / Path(file).name
        cmd = f'touch {dst_file}'
        run_command(cmd)
        temp_cnt = int(os.path.getsize(file) / 4096)
        cmd = f'sudo -S dd if={device} of={dst_file} ibs=4k obs=4k skip={cnt} seek={0} count={temp_cnt} < password'
        run_command(cmd)
        cnt += temp_cnt
        pbar.update(1)
    pbar.close()


def load_data_mp(src, dst, device):
    cnt = 0
    FT.mkPath(dst)
    files = FT.getAllFiles(src)
    tm = TaskManager(processes=8, queue_size=4, callback=None)
    pbar = tqdm(total=len(files))
    for file in files:
        dst_file = Path(dst) / Path(file).name
        cmd = f'touch {dst_file}'
        run_command(cmd)
        temp_cnt = int(os.path.getsize(file) / 4096)
        cmd = f'sudo -S dd if={device} of={dst_file} ibs=4k obs=4k skip={cnt} seek={0} count={temp_cnt} < password'
        tm.new_task(run_command, cmd)
        cnt += temp_cnt
        pbar.update(1)
    pbar.close()
    tm.close()


pe_cycle = 50
retention = 30


def intel_670p():
    type = 'SSD_Intel_670P'
    capacity = 768
    device = '/dev/nvme1n1'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    load_data(src, dst, device)


def kingston_nv1():
    type = 'SSD_Kingston_NV1'
    capacity = 768
    device = '/dev/nvme3n1'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    load_data(src, dst, device)


def seagate_q5():
    type = 'SSD_Seagate_Q5'
    capacity = 384
    device = '/dev/nvme2n1'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    load_data(src, dst, device)


def samsung_870qvo():
    type = 'SSD_SAMSUNG_870QVO'
    capacity = 768
    device = '/dev/sdb'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    load_data(src, dst, device)


def sandisk_redgrey():
    type = 'TF_SanDisk_RedGrey'
    capacity = 96
    device = '/dev/sdd'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    load_data(src, dst, device)


def netac_u185():
    type = 'USB_Netac_U185'
    capacity = 96
    device = '/dev/sdc'

    src = f'data/{capacity}G'
    dst = f'data/{type}/{pe_cycle:03d}pe_{retention:02d}day_{capacity:03d}g'
    load_data(src, dst, device)


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