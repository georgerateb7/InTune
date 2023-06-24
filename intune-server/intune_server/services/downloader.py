from paramiko import SSHClient
from intune_server.models.generation import find_jobs, update_job_by_id
import time

USERNAME = "edj9"
HOST = "dcc-login.oit.duke.edu"
BASE_DIR = "/hpc/group/pfisterlab/edj9"

DONE_STATUS = "Done"


def get_local_wav_path(meta_ix, job, new_level):
    return f"{job['document_id']}_{meta_ix}_{new_level}.wav"


def download_songs():
    while True:
        print("Downloading songs")
        jobs = find_jobs({"status": {"$ne": DONE_STATUS}})

        with SSHClient() as client:
            client.load_system_host_keys()
            client.connect(HOST,
                           username=USERNAME)

            with client.open_sftp() as sftp:
                sftp.chdir(BASE_DIR)
                base_dir_files = sftp.listdir()
                jobs = [job for job in jobs if job["document_id"] in base_dir_files]

                for job in jobs:
                    doc_id = job["document_id"]
                    cwd = f"{BASE_DIR}/{doc_id}"
                    job_dir_files = sftp.listdir(cwd)
                    new_level = job.get('last_level', 3) - 1
                    level_dir = f"level_{new_level}"
                    if "sample_1b" in job_dir_files:
                        cwd += "/sample_1b"
                        if level_dir in sftp.listdir(cwd):
                            cwd += f"/{level_dir}"
                            level_dir_files = sftp.listdir(cwd)
                            wav_files = [f"item_{meta_ix}" for meta_ix in range(len(job["metas"]))]
                            files_to_dl = [file for file in level_dir_files if file in wav_files]
                            if len(files_to_dl) == len(wav_files):
                                for meta_ix in range(len(wav_files)):
                                    local_wav_path = get_local_wav_path(meta_ix, job, new_level)
                                    sftp.get(
                                        f"{cwd}/item_{meta_ix}.wav",
                                        f"static/{local_wav_path}"
                                    )

                                    status = f"Generating level {new_level}"
                                    if new_level == 0:
                                        status = DONE_STATUS
                                    update_dict = {"last_level": new_level,
                                                   "status": status}
                                    update_job_by_id(job["document_id"], update_dict)


            print("Finished Downloading songs")
            time.sleep(60)
