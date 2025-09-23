# spike_pipeline.py
import os
import numpy as np
from functions_get_data import *
from utils_extraction import get_session_type_final
from utils_tt import *
from spike_sorting import *

def create_spike_data(
    sessions,
    base_data_path,
    save_base_path,
    fs=30e3,
    t_pre=0.2,
    t_post=0.5,
    bin_width=0.005,
    freq_min=3
):
    """
    Crée les fichiers spike_clusters et spike_times pour une liste de sessions.
    """
    psth_bins = np.arange(-t_pre, t_post + bin_width, bin_width)

    for session in sessions:
        print(f"Processing session {session}...")
        chemin = os.path.join(base_data_path, session)
        save_path = os.path.join(save_base_path, session)
        os.makedirs(save_path, exist_ok=True)

        # Déterminer les bons channels
        good_clusters_file = os.path.join(chemin, 'headstage_0', 'good_clusters.npy')
        if os.path.exists(good_clusters_file):
            num_channel = np.load(good_clusters_file, allow_pickle=True)
        else:
            num_channel = np.arange(32)
        print(f"Channels: {num_channel}")

        # Charger les données brutes
        neural_data_file = os.path.join(chemin, 'headstage_0', 'neural_data.npy')
        if not os.path.exists(neural_data_file):
            print(f"Neural data missing for session {session}")
            continue
        nd = np.load(neural_data_file, allow_pickle=True)

        # Calcul du nombre minimum de spikes
        duree_session = len(nd[0]) / fs
        nbr_spikes_min = duree_session * freq_min

        # Créer les fichiers spike_times et spike_clusters
        create_spikes_clusters(save_path, num_channel, nbr_spikes_min)
        print(f"Spike data created for session {session}")

