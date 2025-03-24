import axios from "axios";

const BASE_URL = "http://localhost:5000/api/client_insights";

// Fetch most recurring clients
export const fetchMostRecurringClients = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/most_recurring_clients`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching most recurring clients:", error);
    throw error;
  }
};

// Fetch clients with the most purchases
export const fetchClientsWithMostPurchases = async (filters = {}) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/clients_with_most_purchases`,
      {
        params: filters,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching clients with most purchases:", error);
    throw error;
  }
};

// Fetch clients with the most transferred funds
export const fetchClientsWithMostTransferredFunds = async (filters = {}) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/clients_with_most_transferred_funds`,
      {
        params: filters,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching clients with most transferred funds:", error);
    throw error;
  }
};

// Fetch clients with the most received funds
export const fetchClientsWithMostReceivedFunds = async (filters = {}) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/clients_with_most_received_funds`,
      {
        params: filters,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching clients with most received funds:", error);
    throw error;
  }
};

// Fetch cities with the most clients
export const fetchCitiesWithMostClients = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/cities_with_most_clients`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching cities with most clients:", error);
    throw error;
  }
};

// Fetch countries with the most users
export const fetchCountriesWithMostUsers = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/countries_with_most_users`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching countries with most users:", error);
    throw error;
  }
};
