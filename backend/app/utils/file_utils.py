import os
import shutil
import uuid
from pathlib import Path


UPLOAD_DIR = "app/uploads"
PROJECT_DIR = "app/indexed_projects"


os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROJECT_DIR, exist_ok=True)


def save_uploaded_zip(file):

    filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return filepath


def create_project_folder(project_name: str):

    folder = os.path.join(
        PROJECT_DIR,
        project_name.replace(" ", "_")
    )

    os.makedirs(folder, exist_ok=True)

    return folder


def create_clone_folder():

    folder = (
        Path(PROJECT_DIR)
        / str(uuid.uuid4())
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return str(folder)