# DataHunters solution for challenge #8 Empower Citizens with Open Government Data

## Features planned

## Features Done

## Technologies used

### Frontend

### Backend

## What have failed

### Deployment of valueNet

First, we tried to deploy ValueNet on Azure.
This, simply because azure offered a container environment with GPU support, which is needed by ValueNet.
In the [ValueNet]:"https://github.com/brunnurs/valuenet.git" repository, there is a `docker-compose` file which will set up directly all needed components:

* PostgresDB with the sample datasets provided by FOITT for Hack Zürich
* Adminer
* ValueNet with a pretrained model for the Hack Zürich dataset

Thus, the idea was to use docker-compose directly in the Azure cloud.
This was not directly possible due to the fact that there is no (compatible) option in docker-compose to request gpus resources.
Therefore, the ValueNet would not have GPU access and thus will not work.
We translated the docker-compose file into a Azure CLI compatible yaml file which should (in theory) set up the similar environment as docker-compose would had.
Afterwards, we recognized that on Azure we only have access NVIDIA Tesla K80 GPUs which were not supported anymore by the used nvidia-pytorch docker image used by ValueNet.
We could have downgraded the version but since the last supported version was more than two years old, we decided against this because the we would surely run into conflicts.

As a next provider IBM cloud came into our mind.
There, the upgrade from the free to the pay-as-you-go account failed (for several team members) and thus, we could not collect our free 200$ credits which we would needed in order to create a VM with GPU capabilities.

Deploying on AWS was not usable as well because they do not offer free tier instances with GPU support.

At Google Cloud we also had no luck since there, we could redeem our free credits but the quotas did not allow us to run any instance with GPU support.

With help from the FOITT team, we tried Google Colab.
In the end we brought ValueNet up (at least according to the output from the notebook).
But testing was rather impossible since Google Colab instances are running behind a NAT.
After several ours of debugging and hacking a way around the NAT (Reverse socket via ngrok etc. etc.), we gave up trying deploying our own ValueNet instance.
