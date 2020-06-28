FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /pr201_bot
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libssl-dev libcurl4-openssl-dev libpng-dev libmagick++-dev pandoc r-base python3.7 python3-pip python3-setuptools python3-dev python3-venv python3-wheel texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra texlive-lang-cyrillic texlive-lang-greek
ENV VIRTUAL_ENV=/pr201_bot/bot_env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN R -e "install.packages('exams', dependencies = TRUE)" && R -e "install.packages('ids', dependencies = TRUE)"
COPY requirements.txt ./
RUN pip3 install wheel && pip3 install -r requirements.txt
ADD ./R ./R
COPY ./bot.py ./config.py ./r2pygen.py ./util.py ./
RUN tlmgr init-usertree
ENTRYPOINT ["python3", "bot.py"]