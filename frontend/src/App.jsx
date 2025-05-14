import { useState } from 'react';
import JobForm from './components/JobForm';
import JobTable from './components/JobTable';
import './App.css';

function App() {
  const [refresh, setRefresh] = useState(false);

  return (
    <div className="container">
      <h1>🔍 Backlink Tracker</h1>
      <JobForm onJobCreated={() => setRefresh(!refresh)} />
      <JobTable key={refresh} />
    </div>
  );
}

export default App;
