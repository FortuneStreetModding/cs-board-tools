"""Validity checks for custom music.
"""
from dataclasses import dataclass
from pathlib import Path

from cs_board_tools.schema.descriptor import MapDescriptor
from cs_board_tools.validation.network import get_file_metadata
from cs_board_tools.validation.results import build_results_object


music_content_diff_error = (
    "The music file {file_1} has different "
    "content from the music file {file_2}."
)

music_content_volume_error = (
    "The music file {file_1} has the same "
    "content as the music file {file_2} but "
    "a different volume."
)

mirror_download_size_mismatch_error = (
    "The music files downloaded from each "
    "mirror are not the same. The archive from {domain_1} "
    "is {file_1_size}, but the archive from {domain_2} "
    "is {file_2_size}."
)

missing_gdrive_api_key_error = (
    "In order to run the Music Download test, you must supply "
    "a valid Google Drive API key, as it is needed to download "
    "the files hosted there."
)


@dataclass
class MusicFileMetadata:
    """
    This dataclass holds metadata for a music file.
    """
    file_size: int
    file_hash: str
    file_path: Path
    music: str


bgmVolumeSensitiveHash: dict[str, MusicFileMetadata] = {}
bgm_vol_insensitive_hash: dict[str, MusicFileMetadata] = {}


def handle_file_size_error(mirror_file_size_dict: dict):
    """
    If a file size error has occurred, which is when the files
    downloaded from the Music Download mirrors do not match in
    size, this function handles the processing needed to return
    a proper error message.

    :param mirror_file_size_dict: A dict containing information
        relating to the two music files that were downloaded.
    :type mirror_file_size_dict: dict

    :return: A fully-formatted error message.
    :rtype: str
    """
    formatted_dict = {}
    for key, value in mirror_file_size_dict.items():
        domain = key.replace("https://", "")
        keylist = domain.split("/")
        domain = keylist[0]
        size = int(value)
        # It's in raw bytes for one, so let's try and
        # get this up to MB.
        formatted_dict[f"{domain}"] = (
            f"{round((size / 1024) / 1024, 2)} MB"
        )
    keys = list(formatted_dict)
    values = list(formatted_dict.values())
    domain_1 = keys[0]
    domain_2 = keys[1]
    size_1 = values[0]
    size_2 = values[1]

    return mirror_download_size_mismatch_error.format(
        domain_1=domain_1,
        file_1_size=size_1,
        domain_2=domain_2,
        file_2_size=size_2
    )


def check_music_download(
    descriptor: MapDescriptor = None,
    gdrive_api_key: str = "",
    skip: bool = False
):
    """
    This test downloads the file from each download mirror, and both
    compares their sizes and hashes them to ensure the archives are
    actually the same.

    :param descriptor: A MapDescriptor object representing a board.
    :type descriptor: MapDescriptor

    :param gdrive_api_key: A valid Google Drive API key, which will be
        used to download the music file stored on that service. If not
        supplied, the Music Download check will be skipped.
    :type gdrive_api_key: str, optional

    :param skip: If set to True, the check will be skipped, but a
        valid resultobject with no messages and SKIPPED as its
        status will still be returned.
    :type skip: bool

    :return: A CheckResult object containing the check status as
        well as any messages and additional data.
    :rtype: CheckResult
    """
    if skip or not descriptor:
        return build_results_object(skip=True)
    if not gdrive_api_key:
        return build_results_object(
            messages=[missing_gdrive_api_key_error], skip=True
        )
    if descriptor.music is None:
        return build_results_object()
    if descriptor.music.download is None:
        return build_results_object()

    error_messages = []
    informational_messages = []
    warning_messages = []
    mirrors = []

    cswt_domain = "https://nikkums.io/cswt/"

    # get the music download url
    mirrors = descriptor.music.download

    if mirrors is None:
        return build_results_object()

    if len(mirrors) == 0:
        return build_results_object()

    if not mirrors[0].startswith(cswt_domain):
        error_messages.append(
            "The primary download link for custom music must "
            f"start with `{cswt_domain}`. This means it should "
            "be listed first, above any other mirrors."
        )

    if len(mirrors) < 2:
        informational_messages.append(
            "Boards that require downloading custom music should "
            "define at least two download mirrors. Currently, only "
            "one is defined."
        )
    if len(mirrors) > 1:
        mirrorFileSizeDict = {}

        for mirror in mirrors:
            metadata_results = get_file_metadata(
                mirror, gdrive_api_key
            )

            if hasattr(metadata_results, 'informational_messages'):
                informational_messages.extend(
                    metadata_results.informational_messages
                )

            if metadata_results.status == "OK":
                fileMetadata = metadata_results.data
                fileSize = fileMetadata.file_size
                mirrorFileSizeDict[mirror] = fileSize
                if mirror == mirrors[0]:
                    continue
                if mirrors[0] not in mirrorFileSizeDict:
                    continue
                if mirrorFileSizeDict[mirrors[0]] != fileSize:
                    handle_file_size_error(mirrorFileSizeDict)

    results = build_results_object(
        errors=error_messages,
        messages=informational_messages,
        warnings=warning_messages
    )

    error_messages.clear()
    informational_messages.clear()
    warning_messages.clear()

    return results
