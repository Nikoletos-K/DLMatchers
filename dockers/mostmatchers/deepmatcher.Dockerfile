FROM ubuntu:22.04

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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

# install DeepMatcher
RUN conda create -n deepmatcher python=3.6 -y
SHELL ["conda", "run", "-n", "deepmatcher", "/bin/bash", "-c"]
RUN pip install deepmatcher
RUN mkdir /root/.vector_cache

RUN wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip --directory-prefix=/root/.vector_cache
RUN apt-get update
RUN apt-get install unzip
RUN unzip /root/.vector_cache/wiki.en.zip -d /root/.vector_cache/
RUN rm /root/.vector_cache/wiki.en.vec
RUN rm /root/.vector_cache/wiki.en.zip
WORKDIR /methods
RUN git clone https://github.com/nishadi/deepmatcher-sample.git
