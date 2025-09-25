# main_pipeline.py
from preprocess_save import preprocess_and_save
from waveclus_pipeline import run_waveclus
from utils import * # <-- import de la nouvelle fonction
import os
from create_npy import *
import pandas as pd

#je le fais pour toutes les sessions à la fois 





sheet_ids = {
    "HERCULE": "1sFatSTXO0j3OONKstz7YN-mM04kNMjk_r7zo951yicU"
}

# -------- usage ----------
sessions = []
for sheet_name, sheet_id in sheet_ids.items():
    sessions.extend(get_sessions(sheet_name, sheet_id, session_filter=['playback_block']))


base_data_path = '/auto/data6/eTheremin/HERCULE/'
save_base_path = base_data_path

# Paramètres pour la création des spikes
fs = 30e3
t_pre = 0.2
t_post = 0.5
bin_width = 0.005
freq_min = 3

for session in sessions:
    try:
        session_path = os.path.join(base_data_path, session)
        save_path = os.path.join(session_path, 'spike_sorting')

        # Vérifie si les résultats existent déjà
        spike_clusters_file = os.path.join(save_path, 'ss_spike_clusters.npy')
        spike_times_file = os.path.join(save_path, 'ss_spike_times.npy')

        if os.path.exists(spike_clusters_file) and os.path.exists(spike_times_file):
            print(f"Résultats déjà présents pour {session}, passage...")
            continue  # passe cette session

        # Étape 1 : prétraitement et sauvegarde des fichiers .mat
        preprocess_and_save(session_path)

        # Étape 2 : clustering Wave_Clus
        run_waveclus(session_path, save_path)

        # Étape 3 : création des fichiers spike_times et spike_clusters
        create_spike_data(
            sessions=[session_path],
            base_data_path=base_data_path,
            save_base_path=save_base_path,
            fs=fs,
            t_pre=t_pre,
            t_post=t_post,
            bin_width=bin_width,
            freq_min=freq_min
        )

    except Exception as e:
        print(f"Session {session} already spike sorted: {e}")
        pass