This page is intended to add instruction for how to clone the msLLM repo and how to lunch phi1.5 model. This page is a work in progress.


# **Onboarding process:**

- All FTE's have EMU accounts created, all others will need to join [THIS](https://outlook-sdf.office.com/people/group/service.microsoft.com/ghecemu-innersource) group and wait 1hr for replication. This is not managed by this project.
- You will need to belong to an EMU organization. Our organization is technology-and-research. [More info](https://eng.ms/docs/more/github-inside-microsoft/troubleshoot/get-started)
- You will need to join the msLLM-contributors group above 

Once you are onboarded you should be able to see the [msLLM github repo](https://github.com/technology-and-research/msLLM) after authenticating with your microsoft creds.

# **How to clone msLLM repo into a Linux box**

- First create a SSH key on the Linux node you want to clone this repo or use of of your existing ssh keys by running:



`ssh-keygen`

- paste your public SSH key to github and then authorize SSH key access by navigating to Settings in your github on top right corner 
![image.png](/.attachments/image-b326caf8-5317-4ac9-9e3e-28737b5a218b.png)

then click on SSH and GPG keys 

![image.png](/.attachments/image-5b876c43-1ab8-418f-8533-f44801c5a3fd.png)

then click on new SSH key and paste your public key there

![image.png](/.attachments/image-4854f290-b491-4b4f-a6fd-3734a86c32e2.png)

Then click on configure SSO and then click on authorize

![image.png](/.attachments/image-23be8918-e7ac-4a15-a78d-e924c31704b6.png)

Once above is done then you should be able to clone the repo by running:

`git clone git@github.com:technology-and-research/msLLM.git`



# **VLLM installation** 

now that you cloned the repo it is time to install vLLM the requirments are as follow:

- OS: Linux

- Python version: 3.8 – 3.11

- GPU: compute capability 7.0 or higher (e.g., V100, T4, RTX20xx, A100, L4, etc.)
- Nvidia Driver ( All GCR nodes must come with nvidia driver via our congiuration management in case it does not you should be able to install via :


```
sudo apt install -y nvidia-driver-535-server nvidia-headless-535-server nvidia-dkms-535-server nvidia-headless-no-dkms-535-server libnvidia-compute-535-server libnvidia-cfg1-535-server nvidia-compute-utils-535-server nvidia-utils-535-server nvidia-fabricmanager-535
```



- Nvidia CUDA toolkit ( must be installed on most GCR nodes but if it is note follow this [link](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local) to install it



**Build from source**

 
```
cd msLLM
pip install -e .  # This may take 5-10 minutes.
```

Once done if successful you should see this 

![image.png](/.attachments/image-e7f2b495-818b-402b-86ba-a9ead6d4094c.png)


If your built was not successful due to this error:

RuntimeError:
      The detected CUDA version (11.5) mismatches the version that was used to compile
      PyTorch (12.1). Please make sure to use the same CUDA versions.

run below command and then run the build command for vllm again:

 
```
 export CUDA_HOME=/usr/local/cuda-12   # replace cuda-12 with the cuda version that is installed n your system ls /usr/local/cuda
 export PATH=${CUDA_HOME}/bin:${PATH}
 export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:$LD_LIBRARY_PATH
```



**Lets run phi1.5 model now**


Start the server API of course change the IP address to the ip address of the Linux box yo are running this model:

`python3.9 -m vllm.entrypoints.openai.api_server --model microsoft/phi-1_5 --trust-remote-code --port 8000 --host 10.185.170.64`


**for multiple GPU** you can user  --tensor-parallel-size 2 (change the number to actual number of GPU that your machine has in tis example node has 2 GPUs)

` python3.9 -m vllm.entrypoints.openai.api_server --model microsoft/phi-1_5  --tensor-parallel-size 2 --trust-remote-code --port 8000 --host 10.185.170.64`




![image.png](/.attachments/image-a38382ff-a091-4b28-a7f7-2c71ed95853a.png)

This server can be queried in the same format as OpenAI API. For example:

`curl http://localhost:8000/v1/models`

Query the model with input prompts:

` curl  http://10.185.170.64:8000/v1/completions -H "Content-Type: application/json" -d '{ "model": "microsoft/phi-1_5", "prompt": "San Fransisco is", "max_tokens":100, "temperature":0.8 }'`

![image.png](/.attachments/image-51c24487-57ab-4509-a99f-6d2fdde65245.png)




