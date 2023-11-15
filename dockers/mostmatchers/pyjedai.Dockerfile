FROM ubuntu:22.04

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install build essentials
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc

RUN wget  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p  /opt/conda -u && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean --packages && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV PATH /opt/conda/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/cuda-11.6/lib64:/usr/local/cuda-11.6/extras/CUPTI/lib64:$LD_LIBRARY_PATH

RUN conda create -n p39 python=3.9 -y
SHELL ["conda", "run", "-n", "p39", "/bin/bash", "-c"]

# WORKDIR /pyjedai_scripts
# COPY ./test_pyjedai.py /pyjedai_scripts
RUN pip install --use-pep517 pyjedai 
# CMD ["python", "test_pyjedai.py --data_dir=../data/abt_buy"]
