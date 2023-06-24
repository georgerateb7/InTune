from intune_server.models import intune_db
from bson.objectid import ObjectId


def insert_job(job):
    with intune_db() as db:
        return db["jobs"].insert_one(job)


def update_job_by_id(_id, updates):
    with intune_db() as db:
        return db["jobs"].update_one({"_id": ObjectId(_id)}, {"$set": updates})


def find_jobs(query=None):
    if query is None:
        query = {}

    with intune_db() as db:
        jobs = list(db["jobs"].find(query))
        return [
            dict(
                **job,
                date=str(job["_id"].generation_time),
                document_id=str(job["_id"])
            ) for job in reversed(jobs)
        ]
