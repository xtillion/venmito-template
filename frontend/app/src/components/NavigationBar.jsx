import React from "react";
import { Link } from "react-router-dom";

const NavigationBar = () => {
  return (
    <nav
      style={{
        marginBottom: "20px",
        backgroundColor: "#f4f4f4",
        padding: "10px",
      }}
    >
      <Link to="/" style={{ marginRight: "15px", textDecoration: "none" }}>
        Home
      </Link>
      <Link
        to="/client-insights"
        style={{ marginRight: "15px", textDecoration: "none" }}
      >
        Client Insights
      </Link>
      <Link to="/item-insights" style={{ textDecoration: "none" }}>
        Item Insights
      </Link>
    </nav>
  );
};

export default NavigationBar;
