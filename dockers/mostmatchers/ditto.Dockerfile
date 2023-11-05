# FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
FROM ubuntu:22.04

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p  /opt/conda -u && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean --packages && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV PATH /opt/conda/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/cuda-11.6/lib64:/usr/local/cuda-11.6/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# # install GNEM
RUN conda create -n p39 python=3.9 -y
SHELL ["conda", "run", "-n", "p39", "/bin/bash", "-c"]
RUN conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
RUN pip list
RUN pip install pandas pytorch_transformers tensorboard scikit-learn

WORKDIR /methods
RUN git clone https://github.com/nishadi/GNEM.git

# install DITTO
RUN conda create -n p377 python=3.7.7 -y
SHELL ["conda", "run", "-n", "p377", "/bin/bash", "-c"]
RUN conda install pytorch=1.8.0 cudatoolkit=11.1 nvidia-apex -c pytorch -c conda-forge -y

WORKDIR /methods
RUN git clone https://github.com/nishadi/ditto.git
WORKDIR /methods/ditto
RUN sed -i '8d' requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg
RUN pip install tensorboardX nltk
RUN python -m nltk.downloader stopwords

SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
