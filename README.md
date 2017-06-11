## Local Development

### Prerequisites - Debian Stretch

```sh
sudo apt-get update
sudo apt-get install -y \
    build-essential libsndfile-dev libmpg123-dev \
    python3 python3-venv ffmpeg rabbitmq-server
```

### Prerequisites - OS X

```sh
brew install libsndfile mpg123 python3
brew install rabbitmq
brew services start rabbitmq
```

### DynamicAudioNormalizer

Install https://github.com/lordmulder/DynamicAudioNormalizer:

```sh
git clone https://github.com/lordmulder/DynamicAudioNormalizer.git
cd DynamicAudioNormalizer
make MODE=minimal
```

### Clone Repository

```sh
git clone https://github.com/abhayagiri/youtube-sync
cd youtube-sync
python3 -m venv venv
venv/bin/pip install --upgrade setuptools pip
venv/bin/pip install --upgrade -r requirements.txt
```

### Edit Configuration

TODO

## Server Install

```sh
curl https://raw.githubusercontent.com/abhayagiri/youtube-sync/master/server/install | sudo bash
```

Add `/home/youtube-sync/.ssh/id_rsa.pub` to the destination server's `authorized_keys`.
