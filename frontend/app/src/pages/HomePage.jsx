import React from "react";
import { Link } from "react-router-dom";

const LandingPage = () => {
  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Welcome to Venmito's Insights Dashboard</h1>
      <p>Navigate to the available insights below:</p>
      <nav>
        <ul style={{ listStyleType: "none", padding: 0 }}>
          <li style={{ margin: "10px 0" }}>
            <Link
              to="/client-insights"
              style={{ fontSize: "18px", textDecoration: "none" }}
            >
              Client Insights
            </Link>
          </li>
          <li style={{ margin: "10px 0" }}>
            <Link
              to="/item-insights"
              style={{ fontSize: "18px", textDecoration: "none" }}
            >
              Item Insights
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default LandingPage;
