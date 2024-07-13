import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';

jest.mock('axios');

test('renders upload button', () => {
  render(<App />);
  const uploadButton = screen.getByText(/upload/i);
  expect(uploadButton).toBeInTheDocument();
});

test('renders generate and mint buttons after file upload', async () => {
  const file = new File(['dummy content'], 'sample_video.mp4', { type: 'video/mp4' });

  axios.post.mockResolvedValue({
    data: {
      video_uri: 'ipfs://generated-video-uri'
    }
  });

  render(<App />);

  const fileInput = screen.getByLabelText(/upload/i);
  fireEvent.change(fileInput, {
    target: { files: [file] }
  });

  const generateButton = screen.getByText(/generate video/i);
  fireEvent.click(generateButton);

  await waitFor(() => screen.getByText(/mint nft/i));

  const mintButton = screen.getByText(/mint nft/i);
  expect(mintButton).toBeInTheDocument();
});
