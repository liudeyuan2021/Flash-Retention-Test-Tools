import os
import argparse
from tool import fileTool as FT
from tool.mpTool import TaskManager
from tqdm import tqdm


def run_command(cmd):
    print(cmd)
    os.system(cmd)


def store_data(src, device):
    cnt = 0
    files = FT.getAllFiles(src)
    pbar = tqdm(total=len(files))
    for file in files:
        cmd = f'sudo -S dd if={file} of={device} ibs=4k obs=4k skip=0 seek={cnt} < password'
        run_command(cmd)
        cnt += int(os.path.getsize(file) / 4096)
        pbar.update(1)
    pbar.close()


def store_data_mp(src, device):
    cnt = 0
    files = FT.getAllFiles(src)
    tm = TaskManager(processes=8, queue_size=4, callback=None)
    pbar = tqdm(total=len(files))
    for file in files:
        cmd = f'sudo -S dd if={file} of={device} ibs=4k obs=4k skip=0 seek={cnt} < password'
        tm.new_task(run_command, cmd)
        cnt += int(os.path.getsize(file) / 4096)
        pbar.update(1)
    pbar.close()
    tm.close()


def intel_670p():
    src = 'data/384G'
    device = '/dev/nvme1n1'
    store_data(src, device)

def kingston_nv1():
    src = 'data/768G'
    device = '/dev/nvme2n1'
    store_data(src, device)

def seagate_q5():
    src = 'data/384G'
    device = '/dev/nvme3n1'
    store_data(src, device)

def samsung_870qvo():
    src = 'data/768G'
    device = '/dev/sdb'
    store_data(src, device)

def sandisk_redgrey():
    src = 'data/96G'
    device = '/dev/sdc'
    store_data(src, device)

def netac_u185():
    src = 'data/96G'
    device = '/dev/sdd'
    store_data(src, device)

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