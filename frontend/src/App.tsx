import { useState } from 'react';
import axios from 'axios';
import { Editor } from '@monaco-editor/react';
import './App.css';

const VIBES = [
  "Make it more professional",
  "Make it more concise (Pythonic)",
  "Add comprehensive docstrings and comments",
  "Translate to JavaScript",
  "Translate to Python",
  "Explain the code step-by-step",
  "Find potential bugs",
];

const LANGUAGES = [
    "python",
    "javascript",
    "typescript",
    "java",
    "csharp",
    "go",
    "html",
    "css",
]

function App() {
  const [inputCode, setInputCode] = useState('# Welcome to Vibecode Editor!\n# Paste your code here.' || '// Welcome to Vibecode Editor!\n// Paste your code here.');
  const [outputCode, setOutputCode] = useState('// Your transformed code will appear here.');
  const [language, setLanguage] = useState('python');
  const [vibe, setVibe] = useState(VIBES[0]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleVibeCheck = async () => {
    setIsLoading(true);
    setError('');
    setOutputCode('// Generating...');

    try {
      const response = await axios.post('http://localhost:8000/api/vibe-check', {
        code: inputCode,
        vibe: vibe,
        language: language,
      });

      if (response.data.error) {
        setError(response.data.error);
        setOutputCode('// An error occurred.');
      } else {
        setOutputCode(response.data.transformed_code);
      }
    } catch (err) {
      let errorMessage = "Failed to connect to the backend. Is it running?";
      if (axios.isAxiosError(err) && err.response) {
        errorMessage = `Error: ${err.response.status} ${err.response.statusText}`;
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      setError(errorMessage);
      setOutputCode(`// Error: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Vibecode Editor</h1>
        <p>Transform your code with an AI-powered vibe check.</p>
      </header>

      <div className="controls-container">
        <div className="control-group">
            <label htmlFor="language-select">Language:</label>
            <select
                id="language-select"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
            >
                {LANGUAGES.map(lang => <option key={lang} value={lang}>{lang}</option>)}
            </select>
        </div>
        <div className="control-group">
          <label htmlFor="vibe-select">Select Vibe:</label>
          <select
            id="vibe-select"
            value={vibe}
            onChange={(e) => setVibe(e.target.value)}
          >
            {VIBES.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>
        <button id="vibe-check-btn" onClick={handleVibeCheck} disabled={isLoading}>
          {isLoading ? 'Vibing...' : 'Vibe Check'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <main className="editor-container">
        <div className="editor-pane">
          <h2>Input</h2>
          <Editor
            height="60vh"
            language={language}
            theme="vs-dark"
            value={inputCode}
            onChange={(value) => setInputCode(value || '')}
            options={{ minimap: { enabled: false } }}
          />
        </div>
        <div className="editor-pane">
          <h2>Output</h2>
          <Editor
            height="60vh"
            language={language}
            theme="vs-dark"
            value={outputCode}
            options={{ readOnly: true, minimap: { enabled: false } }}
          />
        </div>
      </main>
    </div>
  );
}

export default App;