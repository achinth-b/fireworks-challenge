import React, { useState } from 'react';
import axios from 'axios';

const DocumentUpload = () => {
    const [file, setFile] = useState(null);
    const [documentType, setDocumentType] = useState('passport');
    const [status, setStatus] = useState('');
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setError('');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('');
        setError('');

        if (!file) {
            setError('Please select a file to upload');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('documentType', documentType);

        try {
            const response = await axios.post('http://localhost:8000/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            if (response.data) {
                setStatus('File uploaded successfully!');
                setFile(null);
                setError('');
                
                const fileInput = document.querySelector('input[type="file"]');
                if (fileInput) {
                    fileInput.value = '';
                }
            }
        } catch (err) {
            console.log(err)
            if (err.response) {
                setError(err.response.data?.detail || 'Upload failed');
            } else {
                setError('Server connection failed. Please try again.');
            }
            console.error('Upload error:', err);
        }
    };

    return (
        <div className="upload-container">
            <h2>KYC Document Upload</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="documentType">Document Type:</label>
                    <select
                        id="documentType"
                        value={documentType}
                        onChange={(e) => setDocumentType(e.target.value)}
                    >
                        <option value="passport">Passport</option>
                        <option value="DL">Driver's License</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="file">Select Document:</label>
                    <input
                        type="file"
                        id="file"
                        accept="image/*"
                        onChange={handleFileChange}
                    />
                </div>

                <button type="submit">Upload Document</button>
            </form>

            {status && <p className="success">{status}</p>}
            {error && <p className="error">{error}</p>}

            <style>{`
                .upload-container {
                    max-width: 500px;
                    margin: 2rem auto;
                    padding: 2rem;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }

                .form-group {
                    margin-bottom: 1rem;
                }

                label {
                    display: block;
                    margin-bottom: 0.5rem;
                }

                select, input[type="file"] {
                    width: 100%;
                    padding: 0.5rem;
                    margin-bottom: 1rem;
                }

                button {
                    background-color: #0070f3;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #0051cc;
                }

                .success {
                    color: green;
                }

                .error {
                    color: red;
                }
            `}</style>
        </div>
    );
};

export default DocumentUpload;