# 예제 설명

Matter 디바이스를 통제할 수 있는 Manager Thing 예제.

## 사전 준비

### Matter 디바이스 준비

`connectedhomeip` 레포지토리를 클론합니다.

```bash
git clone --recurse-submodules https://github.com/project-chip/connectedhomeip.git $HOME/tools/connectedhomeip
cd $HOME/tools/connectedhomeip
git checkout b516ff43
```

의존성 패키지 설치.

```bash
sudo apt-get update
sudo apt-get install git gcc g++ pkg-config libssl-dev libdbus-1-dev \
     libglib2.0-dev libavahi-client-dev ninja-build python3-venv python3-dev \
     python3-pip unzip libgirepository1.0-dev libcairo2-dev libreadline-dev -y

# Install additional packages only for Raspberry Pi
if grep -q 'Raspbian\|Raspberry Pi OS' /etc/os-release; then
    sudo apt-get install pi-bluetooth avahi-utils -y
fi
```

시스템 재부팅.

```bash
sudo reboot
```

시스템을 재부팅한 후, `connectedhomeip` 레포지토리에서 `all-cluster-app` matter 앱을 빌드합니다.

```bash
cd $HOME/tools/connectedhomeip

# Unalias python
if alias python > /dev/null 2>&1; then
    unalias python
fi

# Build all-cluster-app

# for Ubuntu x64
./scripts/run_in_build_env.sh "./scripts/build/build_examples.py --target linux-x64-all-clusters build"
# for Ubuntu ARM64 or Raspberry Pi OS ARM64
./scripts/run_in_build_env.sh "./scripts/build/build_examples.py --target linux-arm64-all-clusters build"
# for maxOS x64 (Intel mac)
./scripts/run_in_build_env.sh "./scripts/build/build_examples.py --target darwin-x64-all-clusters build"
# for maxOS ARM64 (ARM mac)
./scripts/run_in_build_env.sh "./scripts/build/build_examples.py --target darwin-arm64-all-clusters build"

# output file locate at <connectedhomeip_repo_root>/out/<target_machine>-all-clusters
```

### python-matter-server 설치

`python-matter-server` 레포지토리를 클론합니다.

```bash
git clone https://github.com/thsvkd/python-matter-server.git
```

파이썬 패키지를 설치하기 전에, 가상 파이썬 환경을 비활성화 해야합니다.

```bash
deactivate
pip -V
```

`python-matter-server` 패키지를 설치합니다.

```bash
cd python-matter-server
pip install .
```

옛날 버전의 `chip` 패키지를 삭제합니다.

```bash
pip uninstall home-assistant-chip-clusters
pip uninstall myssix-chip-*
```

`chip` 파이썬 패키지를 빌드하고 설치합니다.

```bash
# go to root directory of connectedhomeip project
cd $HOME/tools/connectedhomeip

# build chip-core and chip-clusters
source ./scripts/activate.sh
VERSION="0.1.0"
chip_python_package_prefix="myssix-chip"
gn gen ./out/python --args=" \
enable_rtti=true \
enable_pylib=true \
chip_config_memory_debug_checks=false \
chip_config_memory_debug_dmalloc=false \
chip_mdns=\"minimal\" \
chip_python_version=\"$VERSION\" \
chip_python_package_prefix=\"$chip_python_package_prefix\" \
"

ninja -C ./out/python chip-core chip-clusters

# install chip-core and chip-clusters
cd out/python/controller/python
for pkg in $(ls myssix_chip_*); do
    pip install "$pkg" --force-reinstall
done
cd -
```

## 실행

```bash
cd manager_thing/matter_manager_thing
python run.py
```

## 옵션

- `-n, --name | default = None`

  Thing의 이름. 이 이름은 Thing을 구분하기위한 ID이기도 하다.

- `-ip --host | default='127.0.0.1'`

  Thing의 ip 주소.

- `-p, --port | default=1883`

  Thing의 port 번호.

- `-ac, --alive_cycle | default=60`

  Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다.

- `-as, --auto_scan | default=True`

  Middleware 자동스캔 기능 활성화 여부.

- `-sc --scan_cycle | default=60`

  Matter 디바이스 스캔 주기.

- `-c --config | default='matter_conf.json'`

  Manager Thing을 실행할 때 로드할 설정 파일 경로.

- `-i --interactive | default=False`

  interactive 모드로 Manager Thing을 실행할 것인지 여부. 해당 모드로 실행하는 경우 matter device을 발견하면 사용자로 부터 commission 코드를 받아 commission을 수행합니다.

## Services

### Value Services & Function Services

- 해당 예제에서 Value Service, Function Service는 Matter 표준에서 기능의 모음인 Cluster 유형에 따라 작성됩니다. Matter 표준에서 Cluster는 Attribute, Command 라는 요소를 제공합니다. Matter 디바이스는 여러 개의 Cluster를 가질 수 있으며, 자신의 Cluster 유형에 따라 여러가지 Attribute, Command를 제공합니다. Attribute는 Matter 디바이스의 특정 속성, 센서 값에 해당하며 예제에서는 Attribute를 Value로 가상화하여 제공합니다. Command는 Matter 디바이스의 특정 기능을 수행하는 함수에 해당하며 예제에서는 Command를 Function으로 가상화하여 제공합니다.
