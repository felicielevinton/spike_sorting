# main_pipeline.py
from preprocess_save import preprocess_and_save
from waveclus_pipeline import run_waveclus
from utils import * # <-- import de la nouvelle fonction
import os
from create_npy import *


#

sessions = ['HERCULE_20250527_SESSION_02/headstage_0/']
base_data_path = '/auto/data6/eTheremin/HERCULE/'
save_base_path = base_data_path + sessions[0]

# Paramètres pour la création des spikes
fs = 30e3
t_pre = 0.2
t_post = 0.5
bin_width = 0.005
freq_min = 3

for session in sessions:
    session_path = os.path.join(base_data_path, session)
    exist = False
    
    if exist == False: 
        # Étape 1 : prétraitement et sauvegarde des fichiers .mat
        preprocess_and_save(session_path)
        
        # Étape 2 : clustering Wave_Clus
        run_waveclus(session_path, os.path.join(session_path, 'spike_sorting'))

    else:
        None
    # Étape 3 : création des fichiers spike_times et spike_clusters
    create_spike_data(
    sessions= [session_path],
    base_data_path=base_data_path,
    save_base_path=save_base_path,
    fs=fs,
    t_pre=t_pre,
    t_post=t_post,
    bin_width=bin_width,
    freq_min=freq_min
    )