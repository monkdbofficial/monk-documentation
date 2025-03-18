![MonkDB](./assets/monk_logo.png)


# MonkDB- A Unified DB Platform

> Monday, March 17, 2025, 7:46 PM IST

## Introduction

MonkDB is a unified database platform which supports the below workloads.

- Timeseries workloads.
- Vector Workloads.
- Document (JSON) workloads.
- Full Text Search workloads.
- Geospatial workloads.
- Blob (object) workloads.

Users can query using `psql`/`postgresql` **sql** statements or our query HTTP API. 

Users can also try out our SDK. It is highlighted in this [file](requirements.txt).

We shall be releasing SDK support for other stacks as well.

- [![Released](https://img.shields.io/badge/Python-Released-brightgreen)](https://pypi.org/project/monkdb/)
- ![WIP](https://img.shields.io/badge/JS%2FTS-WIP-yellow) 
- ![TODO](https://img.shields.io/badge/Rust-TODO-lightgrey) 
- ![TODO](https://img.shields.io/badge/Java-TODO-lightgrey) 
- ![TODO](https://img.shields.io/badge/Golang-TODO-lightgrey) 

However, users can also leverage postgresql or ORM libraries of their respective stacks.

--- 

## Directory Structure

To follow the instructions of MonkDB, please traverse through the below directories.

- `documentation`- It has instructions on how to work with multi-model data in MonkDB. It also has simulation scripts with synthetic data. We shall be segregating this by language once other SDKs release.
- `sql`- It has usage instructions on how to use MonkDB's SQL commands and create SQL statements. It is WIP.
- `advanced_concepts`- It has usage instructions on dealing with advanced concepts using MonkDB. It is WIP.

---

## Running the simulation of MonkDB

- If you are working in **MacOS** or **Linux** environments, please run [this](get-started.sh) **shell** script.
- However, if you are working in **MS Windows** environment, please run [this](get-started.bat) **bat** script. 
  - If you have **powershell** environment, please use this **ps1** [script](get-started.ps1) to execute the simulations.

### Script permission management

#### Linux/MacOS

Use the `chmod` command to grant execute permissions. `cd` into the directory where this shell script is present.

```shell
$ chmod +x get_started.sh
```

Execute the script directly using the below command.
```shell
$ ./get_started.sh
```

Verify that the file has executable permissions using ls -l. Please note that this is optional.
```shell
$ ls -l get_started.sh
```

#### Windows

Batch files are executed natively by the Windows Command Prompt.

Open Command Prompt (`cmd.exe`) and navigate to the directory containing the script.

```commandline
cd path\to\get_started.bat
```

```commandline
get_started.bat
```

To run directly, double-click the `.bat` file in File Explorer.

Ensure you have sufficient permissions to execute scripts in the directory.

#### Powershell

Open PowerShell as Administrator. Run the below command to bypass restrictions for the current session only.

```commandline
powershell -ExecutionPolicy Bypass -File get_started.ps1
```

However, to permanently Change Execution Policy Open PowerShell as Administrator and Check the current execution policy.

```commandline
Get-ExecutionPolicy
```

```commandline
Set-ExecutionPolicy RemoteSigned
```

Confirm by typing `A` (Yes to All) when prompted.

Execution Policy Options:
- **Restricted**: No scripts are allowed (default setting). 
- **AllSigned**: Only signed scripts are allowed. 
- **RemoteSigned**: Local scripts run without restriction, but remote scripts must be signed. 
- **Unrestricted**: All scripts are allowed but with a warning for remote scripts.

Verify the new policy

```commandline
Get-ExecutionPolicy
```

Finally, run our powershell script.

```commandline
.\get_started.ps1
```

---

**Pre-Requisites Before Running Automation Scripts**:

- Ensure, you have spun up an instance in cloud with specs of 16GB RAM and alteast 100GB of SSD. In our test environment, we always spin up `c5.2xlarge` of AWS EC2 instance family. We recommend you to use its equivalent in your preferred environment.
- Please ensure docker engine and psql are installed & active in the spun up instance. For more information, please refer [Chapter-2](./documentation/02_Get_Started.md) in the documentation section.
    + If you prefer localhost, please ensure docker engine is installed and active. (for localhost, and solely for testing)
    + Also check if psql is installed in localhost. If not, please install it.
    + We have added docker and psql checks in the automation script.
- Once the docker engine is active, spin up MonkDB's docker container from its image (post `docker pull`). The instructions are mentioned in [Chapter-3](./documentation/03_Provisioning_MonkDB_Docker_Image.md). Also implement other instructions of chapter-3.
- Replace `xx.xx.xx.xxx` in [config.ini](./documentation/config.ini) with the spun-up instance ip address. Please ensure the instance is accessible from your envionment. 
    + In your security groups or equivalents, please whitelist ports `4200`, `5432`, `HTTP`, and `HTTPS` ports mapped against your source ip address. You must be able to successfully connect & converse with the spun-up instance over these ports. If you want to login to the spun-up instance, also whitelist `SSH` port in ingress connections.
    + If it is local dev environment, please mention `127.0.0.1` or `localhost`. However, ensure the above note is implemented.
- Run [async timeseries](./documentation/timeseries/timeseries_async_data.py) simulation seperately/in standalone mode as it is based on async live streams. You may interrupt the execution using `KeyboardInterruption`. It is not invoked from automation scripts. Run `python3 documentation/timeseries/timeseries_async_data.py` command from the root workspace.
- [Vector simulation](./documentation/vector/vector_ops.py) might take a delay of 30s for the first run and 10-12 seconds from the second run onwards owing to the usage of sentence transformers (ST) from huggingface. ST must be loaded everytime during data embed calls. The operation would be swift if you are using Cohere, OpenAI, etc for embedding. 

