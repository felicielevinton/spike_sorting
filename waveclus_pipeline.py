# waveclus_pipeline.py
import os
import time
import subprocess
import numpy as np

def run_waveclus(
    session_path,
    raw_data_path,
    nbr_channel=32,
    interval_verification=0.5,
    timeout_creation=300
):
    session_name = os.path.basename(session_path)

    headstage_path = os.path.join(session_path, 'headstage_0')
    if os.path.exists(os.path.join(headstage_path, 'good_clusters.npy')):
        good_channels = np.load(os.path.join(headstage_path, 'good_clusters.npy'), allow_pickle=True)
    else:
        good_channels = np.arange(nbr_channel)

    print(f"Good channels for {session_name}: {good_channels}")

    for channel in good_channels:
        fichier_mat = os.path.join(raw_data_path, f'C{channel}.mat')
        fichier_spikes = os.path.join(raw_data_path, f'C{channel}_spikes.mat')
        fichier_times = os.path.join(raw_data_path, f'times_C{channel}.mat')

        # Wave_clus commands
        get_spikes_cmd = f"matlab -nodesktop -nosplash -batch \"cd('{raw_data_path}'); Get_spikes('{fichier_mat}');\""
        do_clustering_cmd = f"matlab -nodesktop -nosplash -batch \"cd('{raw_data_path}'); Do_clustering('{fichier_spikes}');\""

        try:
            print(f"Executing Get_spikes for channel {channel}...")
            with open('log_get_spikes.txt', 'a') as log_file:
                subprocess.run(get_spikes_cmd, shell=True, check=True, stdout=log_file, stderr=log_file)
        except subprocess.CalledProcessError as e:
            print(f"Error during Get_spikes for channel {channel}: {e}")
            exit(1)

        while not os.path.exists(fichier_spikes):
            print(f"Waiting for {fichier_spikes}...")
            time.sleep(interval_verification)

        try:
            print(f"Executing Do_clustering for channel {channel}...")
            with open('log_do_clustering.txt', 'a') as log_file:
                subprocess.run(do_clustering_cmd, shell=True, check=True, stdout=log_file, stderr=log_file)
        except subprocess.CalledProcessError as e:
            print(f"Error during Do_clustering for channel {channel}: {e}")
            exit(1)

        time_start = time.time()
        while not os.path.exists(fichier_times):
            if time.time() - time_start > timeout_creation:
                print(f"Timeout: {fichier_times} not created.")
                exit(1)
            time.sleep(interval_verification)

        print(f"Channel {channel} processing completed.")
