import subprocess
import shutil
import os
from pathlib import Path
from tqdm import tqdm

class NFSClient:
    def __init__(self):
        pass

    def mount(self, nfs_path: str, local_path: str):
        """Mount an NFS share to a local directory."""
        try:
            # Ensure local_path exists
            Path(local_path).mkdir(parents=True, exist_ok=True)

            # Mount NFS
            subprocess.run(['mount', '-t', 'nfs', nfs_path, local_path], check=True)
            print(f"Mounted {nfs_path} to {local_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to mount {nfs_path} to {local_path}: {e}")
            raise

    def unmount(self, local_path: str):
        """Unmount an NFS share from a local directory."""
        try:
            subprocess.run(['umount', local_path], check=True)
            print(f"Unmounted {local_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to unmount {local_path}: {e}")
            raise

    def copy_file(self, source: str, target: str):
        """Copy a single file from source to target with progress."""
        try:
            with open(source, 'rb') as src_file, open(target, 'wb') as tgt_file:
                total_size = os.path.getsize(source)
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Copying {os.path.basename(source)}") as pbar:
                    while True:
                        buffer = src_file.read(1024 * 1024)  # Read in 1MB chunks
                        if not buffer:
                            break
                        tgt_file.write(buffer)
                        pbar.update(len(buffer))
            print(f"Copied {source} to {target}")
        except Exception as e:
            print(f"Failed to copy {source} to NFS: {e}")
            raise


class MockNFSClient:
    def mount(self, nfs_path: str, local_path: str):
        # Simulate NFS mount by creating a directory
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        print(f"Mock mount of {nfs_path} to {local_path}")

    def unmount(self, local_path: str):
        # Simulate NFS unmount by doing nothing
        print(f"Mock unmount of {local_path}")

    def copy_file(self, source_path: str, local_path: str):
        # Simulate file copy to NFS
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        destination = os.path.join(local_path, os.path.basename(source_path))
        shutil.copy2(source_path, destination)
        print(f"Copied {source_path} to {destination}")
