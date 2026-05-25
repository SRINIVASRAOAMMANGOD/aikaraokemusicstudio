# Git Remote Quick Notes

## Remotes

### github
Main source code repo

URL:
https://github.com/srinivasraoammangod/aikaraokemusicstudio.git

Used for:
- backup
- development
- source code storage

Pull from GitHub:
git pull github main


---

### origin
Hugging Face deployment repo

URL:
https://huggingface.co/spaces/WEBSITEMAN/ai-karaoke-studio

Used for:
- deployment
- hosting app publicly

Push to Hugging Face:
git push origin main


---

## Flow

GitHub -> pull -> Local PC -> push -> Hugging Face


---

## Useful Commands

Show remotes:
git remote -v

Pull latest code:
git pull github main

Push to HF:
git push origin main