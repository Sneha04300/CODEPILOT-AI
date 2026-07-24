import shutil
from pathlib import Path

from git import Repo


class GitHubService:

    @staticmethod
    def clone_repository(
        github_url: str,
        destination: str,
    ):

        destination_path = Path(destination)

        print("GitHub URL:", github_url)
        print("Destination:", destination_path.resolve())

        if destination_path.exists():
            shutil.rmtree(destination_path)

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        Repo.clone_from(
            github_url,
            str(destination_path),
        )

        print("Clone completed successfully.")

        return str(destination_path)