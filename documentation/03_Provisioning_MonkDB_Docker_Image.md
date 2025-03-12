# Running MonkDB on Docker

Create a dedicated network using the below command to manage persistence.

```bash
$ docker network create monkdb
```

Pull our docker image hosted in AWS ECR public repository.

```bash
$ docker pull public.ecr.aws/monkdblabs/monkdblabs/monkdb:2025.3.1
```

The current stable & latest version is `2025.3.1`. However, please update this version in the above 
command whenever we release a new image.

Once you successfully pull our docker image, ensure its presence by running the below command.

```bash
$ docker images
```

It should give an output something like below. 

```bash
$ docker images
REPOSITORY                                    TAG        IMAGE ID       CREATED        SIZE
public.ecr.aws/monkdblabs/monkdblabs/monkdb   2025.3.1   9ff1cd7f2fe1   47 hours ago   907MB
```

Now run the docker image in daemon mode/background mode. 

```bash
$ docker run -d \
  --publish=4200:4200 \
  --publish=5432:5432 \
  --env MONKDB_HEAP_SIZE=1g \
  --net=monkdb \
  --name=monkdb01 \
  9ff1cd7f2fe1 \
  -Cnetwork.host=_site_,_local_ \
  -Cnode.name=monkdb01 \
  -Cauth.host_based.config.0.user=monkdb \
  -Cauth.host_based.config.0.address=_local_,_site_ \
  -Cauth.host_based.config.0.method=trust \
  -Cauth.host_based.config.99.method=password
```

