# iclouded


## installation
i recommend using venv for this so
```bash
python -m venv venv
./venv/bin/pip install -r requirements.txt
```

## configuration
heres the config :3
```toml
[user]
username = "<email>"
password = "<password>"

[options]
location = "~/icloud"
```
^ put this in `iclouded.toml` in the same folder as all the python files


## running
im lazy so you have to just run it with `./venv/bin/python main.py`

HOWEVER if you use fish (as you should) you can use this function:
```fish
function iclouded
    cd <iclouded location>
    ./venv/bin/python main.py
    cd --
end
```
^ `~/.config/fish/functions/iclouded.fish`

you should then be able to just use `iclouded` from wherever
