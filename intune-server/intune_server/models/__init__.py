import contextlib
import pymongo


HOST_NAME = "mongodb+srv://intune-user:intune-pass@intunecluster.qlphb.mongodb.net/intune_db?retryWrites=true&w=majority"


@contextlib.contextmanager
def intune_db():
    client = pymongo.MongoClient(HOST_NAME)

    try:
        yield client["intune_db"]
    except Exception as error:
        print(error)
    finally:
        client.close()
