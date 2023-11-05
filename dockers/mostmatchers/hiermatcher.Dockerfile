# FROM pytorch/pytorch:latest
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

# install HierMatcher
WORKDIR /methods
RUN git clone https://github.com/nishadi/EntityMatcher.git
WORKDIR /methods/EntityMatcher/embedding/
RUN wget https://zenodo.org/record/6466387/files/wiki.en.bin
RUN conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

# # directory needed for DITTO results
# WORKDIR /home/remote/u6852937/projects

# #install HIF-KAT
# WORKDIR /methods
# RUN wget https://zenodo.org/record/7020029/files/em2.tar.gz
# RUN tar -xf em2.tar.gz
# RUN rm em2.tar.gz
# RUN conda create -n em --clone /methods/em2
# RUN rm /root/.vector_cache/wiki.en.zip
# WORKDIR /methods
# RUN git clone https://github.com/gpapadis/HIF-KAT.git
# SHELL ["conda", "run", "-n", "em", "/bin/bash", "-c"]
# WORKDIR /methods/HIF-KAT/dataset/magellan_dataset/
# RUN python 1.bigtable-attrdrop-ind.py
# RUN python 2.mag-table.py
# RUN python 3.stat.py
# RUN python 4.mag.py
# RUN python 5.traditional_feature.py
