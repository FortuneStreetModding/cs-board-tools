"""Validation tests requiring network access live here.
"""
import sys
from dataclasses import dataclass
from datetime import datetime
import requests

from cs_board_tools.validation.results import build_results_object


gdrive_link_malformed_error = (
    "The custom music Google Drive download link is malformed. "
    "It must conform to the following format: "
    "`https://drive.google.com/u/2/uc?id=<some_id>&export=download`"
)


@dataclass
class FileMetadata:
    """
    This dataclass holds metadata for files downloaded from the internet.
    File size and last modified date are the metadata represented by currently.
    """
    file_size: int
    last_modified: datetime


def get_file_metadata(url: str, gdrive_api_key: str) -> FileMetadata:
    """
    This function downloads files and returns metadata about them.

    :param url: The web address of a file to download.
    :type url: str

    :param gdrive_api_key: A valid Google Drive API key. Used when the file
        to be downloaded is hosted on that service. Not otherwise used.
    :type gdrive_api_key: str

    :return: A FileMetadata object representing the metadata of the object
        whose URL was passed into the function.
    :rtype: FileMetadata
    """
    error_messages = []
    informational_messages = []
    warning_messages = []
    metadata = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 "
        "Safari/537.36"  # NOQA
    }
    try:
        sess = requests.session()
        size = -1
        if "drive.google.com" in url:
            if not gdrive_api_key:
                message = (
                    "To run the Music Download test against mirrors that "
                    "include Google Drive, you must supply a valid Google "
                    "Drive API key."
                )
                informational_messages.append(message)
                return build_results_object(
                    messages=informational_messages,
                    skip=True
                )
            if "id=" not in url:
                error_messages.append(gdrive_link_malformed_error)
                return build_results_object(
                    errors=error_messages,
                    messages=informational_messages
                )

            headers["Accept"] = "application/json"
            fileId = url.split("id=")[1].split("&")[0]
            res = sess.get(
                f"https://www.googleapis.com/drive/v3/files/{fileId}"
                "?alt=json&fields=size,modifiedTime"
                f"&key={gdrive_api_key}"
            )

            data = res.json()

            if "error" in data:
                error = (
                    f"The custom music archive at `{url}`"
                    "could not be downloaded. "
                )

                if "message" in data["error"]:
                    error_messages.append(
                        f"{error} ",
                        f"(Error from server: {data['error']['message']})"
                    )
                else:
                    error_messages.append(error)
            else:
                size = int(data["size"])
                lastModifiedStr = data["modifiedTime"]
                # 2022-01-06T14:11:48.000Z
                lastModifiedDate = datetime.strptime(
                    lastModifiedStr, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                metadata = FileMetadata(size, lastModifiedDate)
        else:
            res = sess.head(
                url,
                headers=headers,
                stream=True,
                verify=True,
                allow_redirects=True
            )
            size = int(res.headers.get("Content-Length", 0))
            lastModifiedStr = res.headers.get("Last-Modified", 0)
            # Thu, 17 Mar 2022 12:28:08 GMT
            if lastModifiedStr == 0:
                error_messages.append(
                    f"The custom music archive at `{url}` "
                    "could not be downloaded."
                )
            else:
                lastModifiedDate = datetime.strptime(
                    lastModifiedStr, "%a, %d %b %Y %H:%M:%S %Z"
                )
                metadata = FileMetadata(size, lastModifiedDate)

        results = build_results_object(
            errors=error_messages,
            messages=informational_messages,
            warnings=warning_messages,
            data=metadata
        )
        return results
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        error_messages.clear()
        informational_messages.clear()
        warning_messages.clear()
        sess.close()
