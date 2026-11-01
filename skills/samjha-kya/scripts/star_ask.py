"""Decide whether to show the one-time star invitation after a finished deck.

    python3 star_ask.py

Prints one JSON line. "ask": true appears at most once per machine: the invitation is recorded
before it is shown, in a file outside the skill folder, so reinstalls and updates keep it.
Deleting that file, or using another machine, resets it. Any existing record (even a broken one),
storage that cannot be written, or a failed GitHub check means "ask": false.

"mode" is "star" when the GitHub CLI is signed in (the agent may star for the user after an
explicit yes that names the repo and the account) and "link" otherwise (show the link only).
"""
import json
import os
import pathlib
import shutil
import subprocess
import time

REPO = "amishah1998/samjha-kya"
URL = f"https://github.com/{REPO}"


def state_file():
    base = os.environ.get("SAMJHA_KYA_STATE") or os.environ.get("XDG_STATE_HOME") or str(pathlib.Path.home() / ".local" / "state")
    return pathlib.Path(base) / "samjha-kya" / "star-invite.json"


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, timeout=15)


def github_status():
    """("star", login) if signed in and not starred yet, ("link", None) if not signed in, None to skip."""
    if not shutil.which("gh"):
        return "link", None
    try:
        who = gh("api", "user", "--jq", ".login")
        if who.returncode != 0 or not who.stdout.strip():
            return "link", None
        login = who.stdout.strip()
        starred = gh("api", "-i", f"user/starred/{REPO}")
    except (OSError, subprocess.SubprocessError):
        return None
    status = starred.stdout.split(None, 2)[1] if starred.stdout.startswith("HTTP/") else ""
    if status == "204":
        return None
    if status == "404":
        return "star", login
    return None


def claim(path):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError:
        return False
    with os.fdopen(fd, "w") as f:
        json.dump({"repo": REPO, "invited_at": int(time.time())}, f)
    return True


def main():
    path = state_file()
    out = {"ask": False, "repo": REPO, "url": URL}
    if path.exists():
        out["reason"] = "already invited on this machine"
    else:
        status = github_status()
        if status is None:
            out["reason"] = "already starred or GitHub check failed"
        elif not claim(path):
            out["reason"] = "already invited or state not writable"
        else:
            out.update(ask=True, mode=status[0], account=status[1])
    print(json.dumps(out))


if __name__ == "__main__":
    main()
