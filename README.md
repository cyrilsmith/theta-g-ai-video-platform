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
   - Clone the project repository from GitHub to your local machine.

2. **Set up the backend environment:**
   - Create a virtual environment and install the required Python packages including TensorFlow, Flask, Flask-CORS, Flask-JWT-Extended, MoviePy, and pytest.

3. **Train the AI model:**
   - Prepare your dataset of video frames and labels.
   - Build and train the model using the dataset.
   - Save the trained model to a file.

4. **Run the server:**
   - Start the Flask server to handle API requests.

### Smart Contract Deployment

1. **Set up the smart contract environment:**
   - Install Foundry, a powerful toolkit for Ethereum development.
   - Initialize the project and configure Foundry for your development environment.

2. **Compile and deploy the contract:**
   - Compile the smart contract.
   - Deploy the smart contract to the Ethereum network using a script and your private key.

### Frontend Deployment

1. **Set up the frontend environment:**
   - Create a React application and install the necessary packages including Web3, Axios, jwt-decode, jest, @testing-library/react, and @testing-library/jest-dom.

2. **Start the React application:**
   - Run the React development server to start the frontend application.

### Testing

1. **Run backend tests:**
   - Use pytest to run the backend unit tests.

2. **Run integration tests:**
   - Run integration tests to ensure the backend and smart contract interactions work correctly.

3. **Run frontend tests:**
   - Use jest to run the frontend unit tests.

### Additional Resources

- [Theta Documentation](https://docs.thetatoken.org/docs)
- [Theta Hackathon Resources](https://theta2023.devpost.com/resources)

## Conclusion

By combining cutting-edge Generative AI with the decentralized power of Theta Network, this platform offers a robust solution for personalized video content creation and distribution.
