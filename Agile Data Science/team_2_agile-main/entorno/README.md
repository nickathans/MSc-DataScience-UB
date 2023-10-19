If you want to run the app without the need of installing any package you can use the Docker. You need to have installed Docker and run the following command:

docker build -t streamlitapp:latest -f Dockerfile .  
docker run -p 127.0.0.1:8501:8501 streamlitapp:latest

After that we will have an image called streamlitapp in Docker with all the environment requirements needed to run the app.  