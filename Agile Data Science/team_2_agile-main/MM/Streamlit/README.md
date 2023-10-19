To run the app, first install streamlit, Pillow and streamlit-lottie. 
In the prompt, find the folder in which you have the app.py and type in "streamlit run app.py".
The web app should pop up in your browser.

For the Dockerized version, you need to have Docker installed and run the following commands:

docker build -t streamlitapp:latest -f Dockerfile .  
docker run -p 127.0.0.1:8501:8501 streamlitapp:latest