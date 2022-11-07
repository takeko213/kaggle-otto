FROM nvcr.io/nvidia/pytorch:22.10-py3

ARG USERNAME=kaggler
ARG GROUPNAME=kaggler
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID $USERNAME
USER kaggler

RUN pip install --upgrade pip
RUN pip install seaborn==0.12.1
RUN pip install optuna==3.0.3
RUN pip install lightgbm==3.3.3
RUN pip install ipynb_path
RUN pip install python-dotenv
RUN pip install matplotlib-venn
RUN pip install ipywidgets

RUN pip install mlflow
RUN echo "export PATH=\"`python3 -m site --user-base`/bin:\$PATH\"" >> ~/.bashrc
RUN source ~/.bashrc

