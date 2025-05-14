// src/api.js
import axios from 'axios';

const API = 'http://localhost:8000';

export const getJobs = () => axios.get(`${API}/jobs/`);
export const createJob = async ({ url, target_domain, schedule, run_at }) => {
  try {
    const response = await fetch('http://localhost:8000/jobs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url,
        target_domain,
        schedule,
        run_at, // new field for time
      }),
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || 'Failed to create job');
    }

    return await response.json();
  } catch (error) {
    console.error("🚨 Error in createJob:", error.message);
    throw error;
  }
};
export const pauseJob = async (id) => {
  const res = await fetch(`http://localhost:8000/jobs/${id}/pause`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to pause job');
};

export const resumeJob = async (id) => {
  const res = await fetch(`http://localhost:8000/jobs/${id}/resume`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to resume job');
};

export const cancelJob = async (id) => {
  const res = await fetch(`http://localhost:8000/jobs/${id}/cancel`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to cancel job');
};