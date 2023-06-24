import os

from paramiko import SSHClient, AuthenticationException
import uuid
import time
import json
from scp import SCPClient
from pathlib import Path
from intune_server.models.generation import insert_job, update_job_by_id, find_jobs
from intune_server.services.spotify import get_spotify_username
from intune_server.services.downloader import get_local_wav_path
import os


USERNAME = "edj9"
HOST = "dcc-login.oit.duke.edu"
BASE_DIR = "/hpc/group/pfisterlab/edj9"

SAMPLING_RATE = 44100


def get_all_jobs():
    songs = []
    # parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    parent_dir = os.getcwd()
    static_dir = os.path.join(parent_dir, "static")

    for job in find_jobs():
        for meta_ix, meta in enumerate(job["metas"]):
            meta["wavs"] = []
            meta["mode"] = job["mode"]
            meta["sample_length_in_seconds"] = job["sample_length_in_seconds"]
            meta["spotify_username"] = job.get("spotify_username", "Unknown")
            meta["status"] = job.get("status", "Unknown")
            meta["slurm_job_id"] = job.get("slurm_job_id", "Unknown")
            for level in reversed(range(3)):
                wav_name = get_local_wav_path(meta_ix, job, level)
                wav_path = os.path.join(static_dir, wav_name)
                if os.path.exists(wav_path):
                    meta["wavs"].append(wav_name)
            songs.append(meta)

    return songs


def execute_generate_job(sample_length_in_seconds=20,
                         meta_list=None,
                         levels=1,
                         track=None):
    if meta_list is None:
        meta_list = []

    # mode = "primed" if track is not None else "ancestral"
    mode = "ancestral"
    with SSHClient() as client:
        client.load_system_host_keys()
        client.connect(HOST,
                       username=USERNAME)
        # with SCPClient(ssh.get_transport()) as scp:
        #     music_file = Path("/Users/loaner/Downloads/africa-toto.wav")
        #     scp.put(music_file, "~/africa-toto.wav")

        metas_json = [{
            "artist": meta["artist"],
            "genre": meta["genre"],
            "lyrics": meta["lyrics"].replace("'", ""),
            "total_length": sample_length_in_seconds * SAMPLING_RATE,
            "offset": 0
        } for meta in meta_list]
        metas = json.dumps(metas_json)

        document = dict(
            spotify_username=get_spotify_username(),
            mode=mode,
            metas=metas_json,
            sample_length_in_seconds=sample_length_in_seconds,
            track=track,
            slurm_job_id="",
            levels=levels,
            last_level=3,
            status="Queued"
        )
        doc_id = insert_job(document).inserted_id
        job_dir = f"{BASE_DIR}/{doc_id}"
        job_script_path = f"{job_dir}/job.sh"
        job_script = get_job_script(mode=mode,
                                    sample_length_in_seconds=sample_length_in_seconds,
                                    n_samples=len(meta_list),
                                    levels=levels,
                                    metas=metas)

        with client.open_sftp() as sftp:
            sftp.mkdir(job_dir)
            with sftp.open(job_script_path, 'w') as f:
                f.write(job_script)

        stdin, stdout, stderr = client.exec_command(
            f"cd {job_dir};"
            f"/opt/slurm/bin/sbatch job.sh"
        )
        exit_status = stdout.channel.recv_exit_status()  # Blocking call
        print("Exit status:", exit_status)
        out = stdout.read().decode("utf-8")
        err = stderr.read().decode("utf-8")
        slurm_job_id = out.split(" ")[-1].strip()
        update_job_by_id(doc_id, {"slurm_job_id": slurm_job_id})

        return out, err


def get_job_script(mode="ancestral",
                   n_samples=1,
                   sample_length_in_seconds=20,
                   levels=1,
                   metas="[]"):

    return _get_common_directives(n_samples=n_samples,
                                  sample_length_in_seconds=sample_length_in_seconds,
                                  mode=mode,
                                  levels=levels,
                                  metas=metas)


def _get_common_directives(mode="ancestral",
                           sample_length_in_seconds=20,
                           n_samples=1,
                           levels=1,
                           metas="[]"):
    return ("#!/bin/bash\n"
            "#SBATCH -e slurm.err\n"
            "#SBATCH -o slurm.out\n"
            "#SBATCH -p gpu-common\n"
            "#SBATCH --gres=gpu:1\n"
            "#SBATCH --mem=20GB\n"
            "#SBATCH --exclusive\n"
            "source /hpc/group/pfisterlab/edj9/miniconda3/etc/profile.d/conda.sh\n"
            "conda activate jb\n"
            "python ../jukebox/jukebox/sample.py \\\n"
            f"--mode={mode} \\\n"
            f"--sample_length_in_seconds={sample_length_in_seconds} \\\n"
            f"--n_samples={n_samples} \\\n"
            f"--metas='{metas}' \\\n"
            "--model=1b_lyrics \\\n"
            "--name=sample_1b \\\n"
            f"--levels=3 \\\n"
            f"--total_sample_length_in_seconds={sample_length_in_seconds} \\\n"
            f"--sr={SAMPLING_RATE} \\\n"
            "--hop_fraction=0.5,0.5,0.125 \\\n")
