import React, { useState } from 'react';
import Web3 from 'web3';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import contractABI from './contractABI.json';
import styled, { createGlobalStyle } from 'styled-components';

const web3 = new Web3('https://sepolia.infura.io/v3/847ad4f9b62142ea9e09e2e593c9d327');
const contractAddress = '0x3cb22617bdd8275875b358872d2c16c2b7ba011d';
const contract = new web3.eth.Contract(contractABI, contractAddress);

const GlobalStyle = createGlobalStyle`
  body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    margin: 0;
    padding: 0;
    color: #ffffff;
    background-color: #121212;
  }
`;

const Container = styled.div`
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background: #1c1c1e;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
`;

const Title = styled.h1`
  text-align: center;
  color: #bb86fc;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #bb86fc;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  border: 1px solid #bb86fc;
  border-radius: 4px;
  background-color: #2c2c2e;
  color: white;
`;

const Button = styled.button`
  width: 100%;
  padding: 10px;
  background-color: #bb86fc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background-color: #9a69d1;
  }
`;

const Status = styled.div`
  margin-top: 20px;
  padding: 10px;
  background-color: #2c2c2e;
  border: 1px solid #bb86fc;
  border-radius: 4px;
  color: white;
`;

function App() {
    const [videoFile, setVideoFile] = useState(null);
    const [tokenURI, setTokenURI] = useState('');
    const [accessToken, setAccessToken] = useState(null);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [status, setStatus] = useState('');

    const handleUpload = (e) => {
        setVideoFile(e.target.files[0]);
    };

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:5000/login', { username, password });
            setAccessToken(response.data.access_token);
            setStatus('Login successful');
        } catch (error) {
            setStatus('Login failed');
        }
    };

    const handleGenerate = async () => {
        try {
            const formData = new FormData();
            formData.append('file', videoFile);
            setStatus('Processing video...');
            const response = await axios.post('http://localhost:5000/generate', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            setTokenURI(response.data.video_uri);
            setStatus('Video processed successfully');
        } catch (error) {
            setStatus('Video processing failed');
        }
    };

    const handleMint = async () => {
        try {
            const accounts = await web3.eth.getAccounts();
            setStatus('Minting NFT...');
            await contract.methods.createNFT(tokenURI).send({ from: accounts[0] });
            setStatus('NFT minted successfully');
        } catch (error) {
            setStatus('NFT minting failed');
        }
    };

    return (
        <>
            <GlobalStyle />
            <Container>
                <Title>AI Video NFT Platform</Title>
                {!accessToken && (
                    <div>
                        <FormGroup>
                            <Label>Username</Label>
                            <Input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                        </FormGroup>
                        <FormGroup>
                            <Label>Password</Label>
                            <Input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        </FormGroup>
                        <Button onClick={handleLogin}>Login</Button>
                    </div>
                )}
                {accessToken && (
                    <div>
                        <FormGroup>
                            <Label>Upload Video</Label>
                            <Input type="file" onChange={handleUpload} />
                        </FormGroup>
                        <Button onClick={handleGenerate}>Generate Video</Button>
                        {tokenURI && <Button onClick={handleMint}>Mint NFT</Button>}
                    </div>
                )}
                {status && <Status>{status}</Status>}
            </Container>
        </>
    );
}

export default App;
