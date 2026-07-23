import os
import zipfile


class ZipService:

    @staticmethod
    def extract_zip(zip_path: str, extract_to: str):

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        return extract_to

    @staticmethod
    def count_files(folder_path: str):

        total_files = 0

        for root, dirs, files in os.walk(folder_path):
            total_files += len(files)

        return total_files