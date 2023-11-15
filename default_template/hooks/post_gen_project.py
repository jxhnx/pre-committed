import os
import shutil

import requests

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def remove_open_source_files():
    file_names = ["LICENSE"]
    for file_name in file_names:
        os.remove(file_name)


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        os.remove(file_name)


def remove_dotgitlabciyaml_file():
    os.remove(".gitlab-ci.yaml")


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def generate_gitignore():
    print(INFO + "Fetching recent .gitignore rules...")
    urls = [
        "https://www.toptal.com/developers/gitignore/api/dotenv",
        "https://www.toptal.com/developers/gitignore/api/windows",
        "https://www.toptal.com/developers/gitignore/api/macos",
        "https://www.toptal.com/developers/gitignore/api/linux",
    ]

    responses = []

    try:
        for url in urls:
            response = requests.get(url)
            response.raise_for_status()
            responses.append(response.text)
    except requests.exceptions.RequestException as e:
        print(WARNING + f"Error fetching URL: {e}, using cached .gitignore")
        return None

    custom_header = """######################################################
# Custom / project-specific .gitignore
######################################################







######################################################
# Generated .gitignore for .env, Windows, macOS, Linux
######################################################

"""

    combined_gitignore = custom_header + "\n".join(responses)

    with open(".gitignore", "w") as gitignore_file:
        gitignore_file.write(combined_gitignore)


def main():
    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()
    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.ci_tool }}" != "Gitlab":
        remove_dotgitlabciyaml_file()

    if "{{ cookiecutter.ci_tool }}" != "Github":
        remove_dotgithub_folder()

    generate_gitignore()

    print(SUCCESS + "Nice and done!" + TERMINATOR)


if __name__ == "__main__":
    main()