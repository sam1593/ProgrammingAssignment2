**Wine Quality Prediction App**

**UCID: sfd6**

**Name: Samuel Delgado**

GitHub Repo - https://github.com/sam1593/ProgrammingAssignment2

Docker Hub - https://hub.docker.com/repository/docker/sam1593/mlapplication-pa2/

1.    EMR Cluster Configuration:
        Name Your Cluster: Enter "ml-cluster" as the cluster name.
        Node Setup: Choose 1 primary and 3 worker nodes. Disable auto-termination.
        Key Pair: Create and specify a new EC2 key pair for SSH access.
        Assign Roles: Use EMR_DefaultRole for the cluster and EMR_EC2_DefaultRole for EC2 instances.

2.    EC2 Instance Setup:
        Security Group: Add an SSH inbound rule to the master node’s security group for your IP.
        SSH Access: Use Putty with the created EC2 key pair to access the master node.
        Prepare the System: Run sudo yum update and install Flintrock (pip3 install flintrock).
        Configure Flintrock: Run flintrock configure and adjust the ~/.config/flintrock/config.yaml for your cluster settings (e.g., key-name, identity-file, instance-type).

3.    Launching and Managing Cluster:
        Start the Cluster: Execute flintrock launch ml-cluster.
        Access the Cluster: Use flintrock login ml-cluster.
        Install Libraries: On EC2 instances, install pyspark, boto3, and numpy.

4.    Running the Training Model:
        Execute the Spark job to train the model using the data from S3, and save the model to S3.

5.    Single Machine Prediction:
        Setup: Follow initial EC2 setup steps.
        Deploy Script: Upload wineQualityPrediction.py and the dataset.
        Execute Prediction: Run python wineQualityPrediction.py <testdataset.csv>.

6.    Docker Deployment:
        Prepare Docker: Create a Dockerfile and requirements.txt.
        Build and Push: Build the Docker image (docker build -t mlapplication .), tag it, and push to Docker Hub.
        Run Container: Use docker run to deploy the container locally.