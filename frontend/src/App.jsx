import { useMemo, useState } from 'react';

const categoryStyles = {
  recyclable: { label: 'Recyclable', color: 'green' },
  biological: { label: 'Biological', color: 'amber' },
  trash: { label: 'Trash', color: 'red' },
  unknown: { label: 'Unknown', color: 'slate' },
};

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const selected = event.target.files?.[0];
    if (!selected) return;

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setError('');
    setResult(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError('Please choose an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/classify', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Classification failed.');
      }

      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong while classifying the image.');
    } finally {
      setLoading(false);
    }
  };

  const statusText = useMemo(() => {
    if (!result) return 'No item classified yet.';
    const category = categoryStyles[result.classification] || categoryStyles.unknown;
    return `${category.label} · ${result.detected_type}`;
  }, [result]);

  return (
    <main className="page-shell">
      <section className="app-card">
        <div className="header-block">
          <p className="eyebrow">Smart sorting</p>
          <h1>Waste Classifier</h1>
          <p className="tagline">
            Take a photo of a waste item and instantly learn whether it should be recycled,
            composted, or thrown away.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="upload-panel">
          <label htmlFor="image-upload" className="upload-box">
            {preview ? (
              <img src={preview} alt="Selected waste item" className="preview-image" />
            ) : (
              <div className="upload-placeholder">
                <span className="camera-icon">📷</span>
                <strong>Take a photo or upload an image</strong>
                <small>Use your camera on mobile or choose a file from your device.</small>
              </div>
            )}
          </label>

          <input
            id="image-upload"
            type="file"
            accept="image/*"
            capture="environment"
            onChange={handleFileChange}
          />

          <div className="actions">
            <button type="submit" className="primary-btn" disabled={loading || !file}>
              {loading ? 'Classifying...' : 'Classify Waste'}
            </button>
          </div>
        </form>

        {error && <div className="message error">{error}</div>}

        <div className="result-card">
          <div className="result-header">
            <span className="status-dot" />
            <h2>{statusText}</h2>
          </div>

          {result ? (
            <>
              <div className="result-grid">
                <div>
                  <span className="label">Category</span>
                  <strong className={`pill ${result.classification}`}>
                    {categoryStyles[result.classification]?.label || 'Unknown'}
                  </strong>
                </div>
                <div>
                  <span className="label">Detected item</span>
                  <strong>{result.detected_type}</strong>
                </div>
                <div>
                  <span className="label">Confidence</span>
                  <strong>{result.confidence ? `${(result.confidence * 100).toFixed(1)}%` : 'N/A'}</strong>
                </div>
              </div>

              <div className="explanation-box">
                <h3>What to do</h3>
                <p>{result.explanation}</p>
              </div>
            </>
          ) : (
            <p className="empty-state">Your classification results will appear here.</p>
          )}
        </div>
      </section>
    </main>
  );
}

export default App;
