# main_pipeline.py
from preprocess_save import preprocess_and_save
from waveclus_pipeline import run_waveclus
import os

sessions = ['ALTAI_20240918_SESSION_00']
base_data_path = '/mnt/working4/clara/data2/eTheremin/'
save_base_path = base_data_path

for session in sessions:
    session_path = os.path.join(base_data_path, session)
    save_path = os.path.join(save_base_path, session)
    os.makedirs(save_path, exist_ok=True)

    # Étape 1 : prétraitement et sauvegarde
    preprocess_and_save(session_path, save_path)

    # Étape 2 : clustering Wave_Clus
    run_waveclus(session_path, save_path)
