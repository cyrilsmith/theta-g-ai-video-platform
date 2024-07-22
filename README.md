### README.md

# Theta Generative AI Video Platform

## Project Overview

This project is a Generative AI Video Platform that leverages Theta Network technologies to create personalized video content. The platform uses Theta EdgeCloud for efficient model training and Theta blockchain to tokenize generated content as NFTs, ensuring content authenticity and providing new revenue streams for content creators.

## Team Information

- **Name:** Cyril
- **Age:** 18
- **Country:** Ghana
- **Email Address:** attivoecyril@gmail.com
- **Track:** Generative AI

## How the AI Works and Its Functions

### AI Model

The AI model is built using TensorFlow and the VGG16 architecture, which is pre-trained on the ImageNet dataset. The model is fine-tuned for the specific task of generating video frames.

**Key Functions:**

1. **Model Building:**
   - The model uses VGG16 as the base and adds additional layers for customization.
   - The base model's weights are frozen to retain pre-trained knowledge.

2. **Data Preprocessing:**
   - The preprocessing function reads a video file, extracts frames, resizes them, and normalizes pixel values.

3. **Model Training:**
   - The model is trained on a dataset of video frames and labels.

### Backend Server

The backend server is built using Flask and handles user authentication, video processing, and NFT minting.

**Key Endpoints:**

1. **User Authentication:**
   - JWT is used for secure user authentication.
   - Users can log in to receive a JWT token.

2. **Video Generation:**
   - Users can upload a video file, which is processed by the AI model to generate new content.
   - The generated video is concatenated with the input video.

### Smart Contract

The smart contract is written in Solidity and is used to mint NFTs for the generated videos.

**Key Functions:**

1. **NFT Creation:**
   - The `createNFT` function mints a new NFT with a specified token URI.

### Frontend Application

The frontend is built using React and interacts with the backend and smart contract.

**Key Components:**

1. **User Login:**
   - Users can log in to receive a JWT token, which is used for authenticated requests.

2. **Video Upload and Generation:**
   - Users can upload a video, which is sent to the backend for processing.
   - The processed video URI is then displayed, and users can mint it as an NFT.

3. **NFT Minting:**
   - Users can mint the generated video as an NFT on the Theta blockchain.

## How to Deploy and Run

### Backend Deployment

1. **Clone the repository:**
   - Clone the project repository from GitHub to your local machine:
     ```sh
     git clone https://github.com/your-username/theta-generative-ai-video-platform.git
     cd theta-generative-ai-video-platform
     ```

2. **Set up the backend environment:**
   - Create a virtual environment and install the required Python packages:
     ```sh
     python3 -m venv env
     source env/bin/activate
     pip install -r requirements.txt
     ```

3. **Train the AI model:**
   - Prepare your dataset of video frames and labels.
   - Build and train the model using the dataset:
     ```sh
     python train_model.py
     ```
   - Save the trained model to a file.

4. **Run the server:**
   - Start the Flask server to handle API requests:
     ```sh
     python server.py
     ```

### Smart Contract Deployment

1. **Set up the smart contract environment:**
   - Install Foundry, a powerful toolkit for Ethereum development:
     ```sh
     curl -L https://foundry.paradigm.xyz | bash
     foundryup
     ```

2. **Compile and deploy the contract:**
   - Navigate to the contracts directory:
     ```sh
     cd contracts
     ```
   - Compile the smart contract:
     ```sh
     forge build
     ```
   - Deploy the smart contract to the Ethereum network using a script and your private key:
     ```sh
     forge script script/Deploy.s.sol --rpc-url https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID --private-key YOUR_PRIVATE_KEY --broadcast
     ```

### Frontend Deployment

1. **Set up the frontend environment:**
   - Navigate to the client directory and create a React application:
     ```sh
     cd ../client
     npx create-react-app client
     cd client
     ```
   - Install the necessary packages:
     ```sh
     npm install web3 axios jwt-decode jest @testing-library/react @testing-library/jest-dom
     ```

2. **Start the React application:**
   - Run the React development server to start the frontend application:
     ```sh
     npm start
     ```

### Deploying to Google Cloud

1. **Sign Up for Google Cloud Web3 Startup Program:**
   - Go to [Google Cloud Web3](https://cloud.google.com/startup/web3) and sign up for the program.

2. **Set Up Google Cloud SDK:**
   - Install Google Cloud SDK by following the [installation guide](https://cloud.google.com/sdk/docs/install).
   - Initialize the SDK:
     ```sh
     gcloud init
     ```

3. **Create and Configure a Google Cloud Project:**
   - Create a new project in the Google Cloud Console.
   - Enable necessary APIs (e.g., Cloud Storage, Compute Engine).

4. **Containerize the Application:**
   - Create a `Dockerfile` for the AI application.

     **`Dockerfile`**
     ```Dockerfile
     FROM python:3.9-slim

     WORKDIR /app

     COPY requirements.txt requirements.txt
     RUN pip install -r requirements.txt

     COPY . .

     CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
     ```

   - Build the Docker image:
     ```sh
     docker build -t video-generator-app .
     ```

   - Push the Docker image to Google Container Registry:
     ```sh
     gcloud auth configure-docker
     docker tag video-generator-app gcr.io/YOUR_PROJECT_ID/video-generator-app
     docker push gcr.io/YOUR_PROJECT_ID/video-generator-app
     ```

5. **Deploy the Application to Google Cloud:**
   - Create a Kubernetes cluster:
     ```sh
     gcloud container clusters create video-generator-cluster --num-nodes=3
     gcloud container clusters get-credentials video-generator-cluster
     ```

   - Deploy the application using Kubernetes:

     **`deployment.yaml`**
     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: video-generator
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: video-generator
       template:
         metadata:
           labels:
             app: video-generator
         spec:
           containers:
           - name: video-generator
             image: gcr.io/YOUR_PROJECT_ID/video-generator-app
             ports:
             - containerPort: 5000
     ```

     **`service.yaml`**
     ```yaml
     apiVersion: v1
     kind: Service
     metadata:
       name: video-generator-service
     spec:
       selector:
         app: video-generator
       ports:
         - protocol: TCP
           port: 80
           targetPort: 5000
       type: LoadBalancer
     ```

   - Apply the Kubernetes configuration:
     ```sh
     kubectl apply -f deployment.yaml
     kubectl apply -f service.yaml
     ```

6. **Access the Deployed Application:**
   - Get the external IP address of the service:
     ```sh
     kubectl get services
     ```
   - Open the external IP address in your browser to access the application.

### Testing

1. **Run backend tests:**
   - Use pytest to run the backend unit tests:
     ```sh
     pytest test_server.py
     ```

2. **Run integration tests:**
   - Run integration tests to ensure the backend and smart contract interactions work correctly:
     ```sh
     python integration_test.py
     ```

3. **Run frontend tests:**
   - Use jest to run the frontend unit tests:
     ```sh
     npm test
     ```

### How to Use the Platform (Layman's Terms)

1. **Access the Platform:**
   - Open your web browser and go to the URL where the platform is hosted.

2. **Log In:**
   - Enter your username and password to log in to the platform.
   - If you don't have an account, sign up for one.

3. **Upload a Video:**
   - Click the "Upload Video" button.
   - Select a video file from your computer and upload it.

4. **Generate Personalized Content:**
   - After uploading the video, click the "Generate Video" button.
   - The platform will process the video using the AI model to generate personalized content.

5. **Mint an NFT:**
   - Once the video is generated, click the "Mint NFT" button to tokenize the video on the Theta blockchain.
   - You will need to have a cryptocurrency wallet connected to complete this process.

6. **View and Share Your Content:**
   - After minting the NFT, you can view your personalized video and share it with others.

### Additional Resources

- [Theta Documentation](https://docs.thetatoken.org/docs)
- [Theta Hackathon Resources](https://theta2023.devpost.com/resources)

## Conclusion

By combining cutting-edge Generative AI with the decentralized power of Theta Network, this platform offers a robust solution for personalized video content creation and distribution.

Follow these detailed steps to develop, deploy, and run the Theta Generative AI Video Platform, ensuring it meets all functionality requirements and provides a seamless user experience.
