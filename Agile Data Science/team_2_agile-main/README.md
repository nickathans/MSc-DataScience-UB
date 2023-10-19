To run the app, first install streamlit, Pillow and streamlit-lottie. 
In the prompt, find the folder in which you have the app.py and type in "streamlit run app.py".
The web app should pop up in your browser.

For the Dockerized version, you need to have Docker installed and run the following commands:

docker build -t streamlitapp:latest -f Dockerfile . 

docker run -p 127.0.0.1:8501:8501 streamlitapp:latest

After that we will have an image called streamlitapp in Docker with all the environment requirements needed to run the app.  

Once we have it we can run the app as much as wanted creating a new Docker image as follows:

docker build -t streamlitapp_run:latest -f Dockerfile .

docker run -p 127.0.0.1:8501:8501 streamlitapp_run:latest

If we have not done any change in the code it's enough to run the second line. 
