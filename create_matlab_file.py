# preprocess_save.py
import os
import numpy as np
from scipy.io import savemat
import spikeinterface.full as si
import spikeinterface.extractors as se
import matplotlib

matplotlib.use('Agg')

def preprocess_and_save(
    session_path,
    save_path,
    nbr_channel=32,
    chunk_size=10**6,
    fs=30e3
):
    path_f = os.path.join(session_path, 'headstage_0')
    session_name = os.path.basename(session_path)
    print(f"Processing session: {session_name}")

    if os.path.exists(os.path.join(path_f, 'good_clusters.npy')):
        num_channel = np.load(os.path.join(path_f, 'good_clusters.npy'), allow_pickle=True)
    else:
        num_channel = np.arange(nbr_channel)

    all_files_exist = all(os.path.exists(os.path.join(save_path, f'C{k}.mat')) for k in num_channel)
    if all_files_exist:
        print(f"All 'C' files for {session_name} already exist. Skipping...")
        return

    neural_file = os.path.join(path_f, 'neural_data.npy')
    if not os.path.exists(neural_file):
        print(f"No neural data for {session_name} at {path_f}")
        return

    neural_data = np.load(neural_file)
    full_raw_rec = se.NumpyRecording(traces_list=np.transpose(neural_data), sampling_frequency=fs)
    full_raw_rec = full_raw_rec.astype('float32')

    # Common median reference
    recording_cmr = si.common_reference(full_raw_rec, reference='global', operator='median')
    recording_f = si.bandpass_filter(recording_cmr, freq_min=300, freq_max=3000)

    filtered_neural_signal = np.empty((neural_data.shape[1], neural_data.shape[0]), dtype=np.float32)

    for start in range(0, neural_data.shape[1], chunk_size):
        end = min(start + chunk_size, neural_data.shape[1])
        print(f"Chunk processing {start}:{end}")
        chunk_filtered = recording_f.get_traces(start_frame=start, end_frame=end).astype(np.float32)
        filtered_neural_signal[start:end, :] = chunk_filtered

    np.save(os.path.join(save_path, 'filtered_neural_data.npy'), filtered_neural_signal)

    data = filtered_neural_signal.T  # transpose pour format [channels, time]

    for k in num_channel:
        data_C = data[k, :]
        savemat(os.path.join(save_path, f'C{k}.mat'), {'data': data_C, 'sr': fs})
        print(f"Saved C{k}.mat")
