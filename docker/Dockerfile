FROM python

COPY requirements.txt /tmp/requirements.txt

RUN pip install --ignore-installed -r /tmp/requirements.txt && rm /tmp/requirements.txt

RUN apt-get update && apt-get install -y unzip wget apt-transport-https

# DVC installation
RUN wget https://dvc.org/deb/dvc.list -O /etc/apt/sources.list.d/dvc.list
RUN apt-get update && apt-get install -y dvc

RUN useradd -m user -u 1000
RUN echo 'user:user' | chpasswd user

RUN apt-get update && apt-get install -y sudo

ARG GIT_CONFIG_USER_NAME
ARG GIT_CONFIG_EMAIL

WORKDIR /home/dvc-2-iris-demo

RUN echo "user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user
RUN chown -R user /home

USER user

RUN git config --global user.name $GIT_CONFIG_USER_NAME && git config --global user.email $GIT_CONFIG_EMAIL

CMD jupyter lab --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token=''

