FROM streamlitapp
EXPOSE 8501
WORKDIR /app
COPY . /app
COPY data /app
COPY models /app
COPY src /app

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]