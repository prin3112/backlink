// import { useEffect, useState } from 'react';
// import { getJobs } from '../api';

// export default function JobTable() {
//   const [jobs, setJobs] = useState([]);

//   useEffect(() => {
//     getJobs().then((res) => setJobs(res.data));
//   }, []);
// console.log('jobs',jobs)
//   return (
//     <table>
//       <thead>
//         <tr>
//           <th>ID</th>
//           <th>URL</th>
//           <th>Target Domain</th>
//           <th>Status</th>
//           <th>Created</th>
//         </tr>
//       </thead>
//       <tbody>
//         {jobs.map((job) => (
//           <tr key={job.id}>
//             <td>{job.id}</td>
//             <td>{job.url}</td>
//             <td>{job.target_domain}</td>
//             <td>{job.status}</td>
//             <td>{new Date(job.created_at).toLocaleString()}</td>
//           </tr>
//         ))}
//       </tbody>
//     </table>
//   );
// }


import React, { useEffect, useState } from "react";
import axios from "axios";
import BacklinkTable from "./BacklinkTable";
import { pauseJob, resumeJob, cancelJob } from "../api";

const JobTable = () => {
  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState(null);

  const fetchJobs = async () => {
    try {
      const response = await axios.get("http://localhost:8000/jobs/");
      setJobs(response.data);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleAction = async (action, jobId) => {
    try {
      if (action === "pause") await pauseJob(jobId);
      else if (action === "resume") await resumeJob(jobId);
      else if (action === "cancel") await cancelJob(jobId);

      await fetchJobs(); // Refresh list after action
    } catch (err) {
      alert("❌ " + err.message);
    }
  };

  return (
    <div>
      <h2>🗂️ Crawl Jobs</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>URL</th>
            <th>Target Domain</th>
            <th>Status</th>
            <th>Created At</th>
            <th>Backlinks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={job.id}>
              <td>{job.id}</td>
              <td>{job.url}</td>
              <td>{job.target_domain}</td>
              <td>{job.status}</td>
              <td>{new Date(job.created_at).toLocaleString()}</td>
              <td>
                <button onClick={() => setSelectedJobId(job.id)}>View</button>
              </td>
              <td>
                {job.status === "pending" && (
                  <button onClick={() => handleAction("cancel", job.id)}>Cancel</button>
                )}
                {job.status === "running" && (
                  <button onClick={() => handleAction("pause", job.id)}>Pause</button>
                )}
                {job.status === "paused" && (
                  <button onClick={() => handleAction("resume", job.id)}>Resume</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedJobId && (
        <div style={{ marginTop: "2rem" }}>
          <BacklinkTable jobId={selectedJobId} />
        </div>
      )}
    </div>
  );
};

export default JobTable;

