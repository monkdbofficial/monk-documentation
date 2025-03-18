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
- JS/TS
- Rust
- Java
- Golang

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




