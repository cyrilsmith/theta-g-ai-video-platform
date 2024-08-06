import React, { useState } from 'react';
import Web3 from 'web3';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import contractABI from './contractABI.json';

const web3 = new Web3('https://sepolia.infura.io/v3/847ad4f9b62142ea9e09e2e593c9d327');
const contractAddress = '0xYourActualContractAddress';  // Replace with your contract address
const contract = new web3.eth.Contract(contractABI, contractAddress);

function App() {
    const [videoFile, setVideoFile] = useState(null);
    const [tokenURI, setTokenURI] = useState('');
    const [accessToken, setAccessToken] = useState(null);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleUpload = (e) => {
        setVideoFile(e.target.files[0]);
    };

    const handleLogin = async () => {
        const response = await axios.post('http://localhost:5000/login', { username, password });
        setAccessToken(response.data.access_token);
    };

    const handleGenerate = async () => {
        const formData = new FormData();
        formData.append('file', videoFile);
        const response = await axios.post('http://localhost:5000/generate', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        setTokenURI(response.data.video_uri);
    };

    const handleMint = async () => {
        const accounts = await web3.eth.getAccounts();
        await contract.methods.createNFT(tokenURI).send({ from: accounts[0] });
    };

    return (
        <div className="app">
            {!accessToken && (
                <div className="login-container">
                    <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    <button onClick={handleLogin}>Login</button>
                </div>
            )}
            {accessToken && (
                <div className="upload-container">
                    <input type="file" onChange={handleUpload} />
                    <button onClick={handleGenerate}>Generate Video</button>
                    {tokenURI && <button onClick={handleMint}>Mint NFT</button>}
                </div>
            )}
        </div>
    );
}

export default App;
