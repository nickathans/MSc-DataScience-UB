FROM continuumio/miniconda3

RUN apt update
RUN python3 -m pip install --upgrade pip
RUN conda install -c conda-forge -y h5py

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/maciejkula/spotlight.git@master#egg=spotlight
EXPOSE 8501

COPY . /app
COPY data /app
COPY models /app
COPY src /app

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]