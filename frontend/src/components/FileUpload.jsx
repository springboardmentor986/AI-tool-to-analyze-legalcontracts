import React, { useState, useRef } from 'react';
import axios from 'axios';
import { FiUploadCloud, FiFile, FiX } from 'react-icons/fi';
import { useLanguage } from '../contexts/LanguageContext';
import { useTranslation } from '../hooks/useTranslation';

const FileUpload = ({ onAnalysisStart, onAnalysisComplete }) => {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const { language } = useLanguage();
  const { t } = useTranslation();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (selectedFile) => {
    const validTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword',
      'text/plain'
    ];

    if (validTypes.includes(selectedFile.type)) {
      setFile(selectedFile);
    } else {
      alert(t('upload.error', 'Please upload a PDF, DOCX, DOC, or TXT file'));
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileChange(e.target.files[0]);
    }
  };

  const handleRemoveFile = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      alert(t('upload.selectFile', 'Please select a file first'));
      return;
    }

    onAnalysisStart();

    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);  // Send selected language to backend

    try {
      console.log('Sending request to backend...');
      console.log('Language:', language);
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Received response:', response.data);
      
      if (response.data && response.data.error) {
        alert('Backend error: ' + response.data.error);
        onAnalysisComplete(null);
        return;
      }

      onAnalysisComplete(response.data);
    } catch (error) {
      console.error('Error analyzing contract:', error);
      console.error('Error details:', error.response?.data);
      alert(t('messages.error', 'Error analyzing contract: ') + (error.response?.data?.error || error.message));
      onAnalysisComplete(null);
    }
  };

  return (
    <div className="upload-section">
      <div className={`upload-card ${dragActive ? 'drag-active' : ''}`}>
        <div
          className="upload-area"
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <FiUploadCloud className="upload-icon" />
          <h3>{t('upload.title', 'Upload Contract Document')}</h3>
          <p>{t('upload.dragDrop', 'Drag & drop your contract here, or click to browse')}</p>
          <p style={{ fontSize: '0.875rem', opacity: 0.7 }}>
            {t('upload.supported', 'Supports: PDF, DOCX, DOC, TXT')}
          </p>
          <input
            ref={fileInputRef}
            type="file"
            className="upload-input"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileInputChange}
          />
        </div>

        {file && (
          <div className="selected-file">
            <div className="file-info">
              <FiFile className="file-icon" />
              <div>
                <div style={{ fontWeight: 600 }}>{file.name}</div>
                <div style={{ fontSize: '0.875rem', opacity: 0.7 }}>
                  {(file.size / 1024).toFixed(2)} KB
                </div>
              </div>
            </div>
            <button className="btn-remove" onClick={handleRemoveFile}>
              <FiX /> {t('actions.remove', 'Remove')}
            </button>
          </div>
        )}

        {file && (
          <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
            <button className="btn btn-primary" onClick={handleSubmit}>
              🚀 {t('actions.analyze', 'Analyze Contract')}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
