# Planetly PingPong Throttling App

To Run on Dev, create a Virtual environment, then install dependencies in the requirements file
- Run docker-compose up

# Steps to deploy the application to a Kubernetes cluster.

- First step would be to create a k8s cluster : 
- This can be done via many ways, either using the eks module from terraform or manually on Aws or via eksctl from weaveworks 
- Create Cluster control plane
- Create worker nodes and give IAM role to be able to read from AWS ECR
- If CI/CD was integrated into my build steps for example Jenkins then a simple pipeline  after my final commit would trigger a build 
- This build will run the defined steps and finally create a docker image and push this image to an artefact storage for example AWS ECR
- Then I will create a k8s deployment file using an official template and for redundancy create more than 1 replicas(also my ECR url defined as source of image also with a service defined)
- By now of course I would have all dependencies installed too, kubectl, Minikube, etc
- Create namespace to group resources
- Run kubectl apply -f  deployment.yaml.
- Run kubectl get pods after to see if it was successful

This is what I‘d do for deployments, please let me know if it could be done better up to professional standards.

My preferred deployment strategy especially if we running a Three(9s) SLA defined as our availability agreement would be the blue-green method. Here, a complete replica of the staging/environment is created and new image is deployed on this environment. After testing all is good, traffic is then shifted incrementally from the old(blue) to the new(green) environment, of course this seems a bit ambiguous with resources all over the place but I do believe it is a more safer way especially if something goes wrong, Traffic could be shifted back!

Monitoring the service I believe could be done via aws cloudwatch with sns alerts configured and metrics defined with also actions for some alerts like new instance spin up if an alert has to do with an instance possibly failing, also a big fan of prometheus so this too can be utilized! To measure both on network and application level.

