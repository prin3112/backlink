// import { useState } from 'react';
// import { createJob } from '../api';

// export default function JobForm({ onJobCreated }) {
//   const [url, setUrl] = useState('');
//   const [target, setTarget] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     await createJob({ url, target_domain: target });
//     setUrl('');
//     setTarget('');
//     onJobCreated();
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <input
//         type="text"
//         placeholder="URL to crawl"
//         value={url}
//         onChange={(e) => setUrl(e.target.value)}
//         required
//       />
//       <input
//         type="text"
//         placeholder="Target domain"
//         value={target}
//         onChange={(e) => setTarget(e.target.value)}
//         required
//       />
//       <button type="submit">Submit Job</button>
//     </form>
//   );
// }


import { useState } from 'react';
import { createJob } from '../api';

export default function JobForm({ onJobCreated }) {
  const [url, setUrl] = useState('');
  const [target, setTarget] = useState('');
  const [schedule, setSchedule] = useState('once');
  const [runAt, setRunAt] = useState('09:00'); // default time
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await createJob({
        url,
        target_domain: target,
        schedule,
        run_at: schedule !== 'once' ? runAt : null,
      });

      setUrl('');
      setTarget('');
      setSchedule('once');
      setRunAt('09:00');
      onJobCreated();
    } catch (err) {
      setError(err.message || 'Something went wrong.');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="URL to crawl"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Target domain"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          required
        />
        <select value={schedule} onChange={(e) => setSchedule(e.target.value)}>
          <option value="once">Run Once</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>

        {schedule !== 'once' && (
          <input
            type="time"
            value={runAt}
            onChange={(e) => setRunAt(e.target.value)}
            required
          />
        )}

        <button type="submit">Submit Job</button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}
