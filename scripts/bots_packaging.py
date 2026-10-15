"""
Bots packaging lib
"""
import subprocess

from pdm.backend.hooks.version import SCMVersion


# keep the same as fallback_version in pyproject.toml
UNTAGGED_VERSION = "4.0.0"


def format_version(version: SCMVersion) -> str:
    """Format package version.
    {release}
    {release}.postX.dev{last_commit_date}+g#
    {release}.postX+{last_commit_date}+g#
    """
    print("Version:", version.version)
    print("Branch:", version.branch)
    formated = str(version.version)
    if formated in ("0.0", "0.0.0"):
        # a git repository without a version tag (eg bots is a directory in another repository):
        # not "0.0.postN", but the version of this source
        return UNTAGGED_VERSION
    if version.distance:
        print("version.distance:", version.distance)
        formated += f".post{version.distance}"
        formated += "+" if "dev" in formated else ".dev"
        try:
            # Add last commit date: .devYYYYMMDD+g#short
            formated += subprocess.check_output(
                ["git", "log", "-1", "--format=%cd+g%h", "--date=format:%Y%m%d"]
            ).decode().strip()
        except Exception:
            pass
    return formated
