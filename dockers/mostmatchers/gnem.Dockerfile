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

# # install GNEM
RUN conda create -n p39 python=3.9 -y
SHELL ["conda", "run", "-n", "p39", "/bin/bash", "-c"]
RUN conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
RUN pip list
RUN pip install pandas pytorch_transformers tensorboard scikit-learn

WORKDIR /methods
RUN git clone https://github.com/nishadi/GNEM.git

# # install ZeroER
# WORKDIR /methods
# RUN git clone https://github.com/nishadi/zeroer.git
# WORKDIR /methods/zeroer
# RUN conda env create -f environment.yml

# # install DITTO
# RUN conda create -n p377 python=3.7.7 -y
# SHELL ["conda", "run", "-n", "p377", "/bin/bash", "-c"]
# RUN conda install pytorch=1.8.0 cudatoolkit=11.1 nvidia-apex -c pytorch -c conda-forge -y

# WORKDIR /methods
# RUN git clone https://github.com/nishadi/ditto.git
# WORKDIR /methods/ditto
# RUN sed -i '8d' requirements.txt
# RUN pip install -r requirements.txt
# RUN python -m spacy download en_core_web_lg
# RUN pip install tensorboardX nltk
# RUN python -m nltk.downloader stopwords

# SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

# # install EMTransformer
# WORKDIR /methods
# RUN git clone https://github.com/gpapadis/DLMatchers.git
# RUN conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge
# RUN pip install pytorch_transformers scikit-learn tensorboardX pandas transformers

# # install DeepMatcher
# RUN conda create -n deepmatcher python=3.6 -y
# SHELL ["conda", "run", "-n", "deepmatcher", "/bin/bash", "-c"]
# RUN pip install deepmatcher
# RUN mkdir /root/.vector_cache

# RUN wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip --directory-prefix=/root/.vector_cache
# RUN apt-get update
# RUN apt-get install unzip
# RUN unzip /root/.vector_cache/wiki.en.zip -d /root/.vector_cache/
# RUN rm /root/.vector_cache/wiki.en.vec
# RUN rm /root/.vector_cache/wiki.en.zip
# WORKDIR /methods
# RUN git clone https://github.com/nishadi/deepmatcher-sample.git

# # install Magellan
# RUN pip install -U numpy scipy py_entitymatching

# # install HierMatcher
# WORKDIR /methods
# RUN git clone https://github.com/nishadi/EntityMatcher.git
# WORKDIR /methods/EntityMatcher/embedding/
# RUN wget https://zenodo.org/record/6466387/files/wiki.en.bin
# RUN conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

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
