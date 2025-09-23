# main_pipeline.py
from preprocess_save import preprocess_and_save
from waveclus_pipeline import run_waveclus
from spike_pipeline import create_spike_data  # <-- import de la nouvelle fonction
import os

sessions = ['ALTAI_20240918_SESSION_00']
base_data_path = '/mnt/working4/clara/data2/eTheremin/'
save_base_path = base_data_path

# Paramètres pour la création des spikes
fs = 30e3
t_pre = 0.2
t_post = 0.5
bin_width = 0.005
freq_min = 3

for session in sessions:
    session_path = os.path.join(base_data_path, session)
    save_path = os.path.join(save_base_path, session)
    os.makedirs(save_path, exist_ok=True)

    # Étape 1 : prétraitement et sauvegarde des fichiers .mat
    preprocess_and_save(session_path, save_path)

    # Étape 2 : clustering Wave_Clus
    run_waveclus(session_path, save_path)

# Étape 3 : création des fichiers spike_times et spike_clusters
create_spike_data(
    sessions=sessions,
    base_data_path=base_data_path,
    save_base_path=save_base_path,
    fs=fs,
    t_pre=t_pre,
    t_post=t_post,
    bin_width=bin_width,
    freq_min=freq_min
)
