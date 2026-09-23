"""Download a pinned public ARDY snapshot and verify Hub hashes and sizes."""
import hashlib
import json
from pathlib import Path
import ssl
import sys

from pip._vendor import truststore
truststore.inject_into_ssl()
import httpx
from huggingface_hub import HfApi

REPO = "nvidia/ARDY-Core-RP-20FPS-Horizon8"
REVISION = "257a0843a10bf5201065963d7bca2791e9393a7a"


def main():
    destination = Path(sys.argv[1]).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    info = HfApi().model_info(REPO, revision=REVISION, files_metadata=True)
    report = {"repo": REPO, "revision": info.sha, "files": []}
    with httpx.Client(verify=ssl.create_default_context(), follow_redirects=True, timeout=120) as client:
        for item in info.siblings:
            path = (destination / item.rfilename).resolve()
            if not path.is_relative_to(destination):
                raise ValueError("Invalid remote path")
            path.parent.mkdir(parents=True, exist_ok=True)
            expected = item.lfs.sha256 if item.lfs else item.blob_id
            def check(candidate):
                if not candidate.exists() or candidate.stat().st_size != item.size:
                    return False
                if item.lfs:
                    h = hashlib.sha256()
                else:
                    h = hashlib.sha1(f"blob {item.size}\0".encode())
                with candidate.open("rb") as stream:
                    for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                        h.update(block)
                return h.hexdigest() == expected
            if not check(path):
                partial = path.with_name(path.name + ".partial")
                print(f"Downloading {item.rfilename}: {item.size} bytes", flush=True)
                url = f"https://huggingface.co/{REPO}/resolve/{REVISION}/{item.rfilename}"
                with client.stream("GET", url) as response:
                    response.raise_for_status()
                    with partial.open("wb") as stream:
                        for block in response.iter_bytes(1024 * 1024):
                            stream.write(block)
                if not check(partial):
                    raise ValueError(f"Hash/size verification failed: {item.rfilename}")
                partial.replace(path)
            report["files"].append({"name": item.rfilename, "bytes": item.size,
                                    "digest": expected, "algorithm": "sha256" if item.lfs else "git-blob-sha1"})
            print(f"Verified {item.rfilename}", flush=True)
    (destination / "download-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
