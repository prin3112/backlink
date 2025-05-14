// import React, { useEffect, useState } from "react";
// import axios from "axios";

// const BacklinkTable = ({ jobId }) => {
//   const [backlinks, setBacklinks] = useState([]);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchBacklinks = async () => {
//       try {
//         const res = await axios.get(`http://localhost:8000/backlinks?job_id=${jobId}`);
//         setBacklinks(res.data);
//       } catch (error) {
//         console.error("Failed to fetch backlinks:", error);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchBacklinks();
//   }, [jobId]);

//   if (loading) return <p>Loading...</p>;

//   return (
//     <div>
//       <h2>Backlink Results for Job #{jobId}</h2>
//       <table border="1" cellPadding="10">
//         <thead>
//           <tr>
//             <th>Source URL</th>
//             <th>Target URL</th>
//             <th>Rel</th>
//             <th>Title</th>
//           </tr>
//         </thead>
//         <tbody>
//           {backlinks.map((link, index) => (
//             <tr key={index}>
//               <td>{link.source_url}</td>
//               <td>{link.target_url}</td>
//               <td>{link.rel}</td>
//               <td>{link.title}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// };

// export default BacklinkTable;


import React, { useEffect, useState } from "react";
import axios from "axios";

const BacklinkTable = ({ jobId }) => {
  const [backlinks, setBacklinks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBacklinks = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/analytics/${jobId}`);
        setBacklinks(res.data);
      } catch (error) {
        console.error("Failed to fetch backlinks:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBacklinks();
  }, [jobId]);

  if (loading) return <p>Loading backlinks...</p>;

  return (
    <div>
      <h3>🔗 Backlinks for Job #{jobId}</h3>
      <table border="1" cellPadding="8" style={{ width: "100%", marginTop: "1rem" }}>
        <thead>
          <tr>
            <th>Source URL</th>
            <th>Target URL</th>
            <th>Rel</th>
            <th>Title</th>
          </tr>
        </thead>
        <tbody>
          {backlinks.map((link, index) => (
            <tr key={index}>
              <td>{link.source_url}</td>
              <td>{link.target_url}</td>
              <td>{link.rel}</td>
              <td>{link.title}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BacklinkTable;
