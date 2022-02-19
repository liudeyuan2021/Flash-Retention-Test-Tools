import os
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


if __name__ == '__main__':
    '''
    nvme1n1 q5 384gb
nvme2n1 670p 384gb
nvme3n1 nv1 768gb
sdb 870 768gb
sdc 96gb
sdd 96gb
sde 96gb
    '''

    src = 'data/768G'
    device = '/dev/nvme3n1'
    store_data(src, device)