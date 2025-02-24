import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/venmito-felixdasta'; // Update with your actual API URL

export const fetchPeople = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/people`);
    return response.data;
  } catch (error) {
    console.error('Error fetching people:', error.response?.data || error.message);
    throw error;
  }
};

export const fetchPromotedPeople = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/people/promotions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching promoted people:', error.response?.data || error.message);
    throw error;
  }
};


export const fetchTransactions = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/transactions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching transactions:', error.response?.data || error.message);
    throw error;
  }
};

export const fetchPromoInfo = async (personId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/people/${personId}/promotions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching promo info:', error.response?.data || error.message);
    throw error;
  }
};

export const fetchPromotionDetails = async (promotionName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/people/promotions/${promotionName}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching promotion details:", error.response?.data || error.message);
    throw error;
  }
};

export const fetchImprovementSuggestions = async (promotionName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/people/promotions/${promotionName}/improvement-suggestions`);
    return response.data;
  } catch (error) {
    console.error("Error fetching improvement suggestions:", error.response?.data || error.message);
    throw error;
  }
};

export const fetchStoreCustomers = async (storeName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stores/${storeName}/people`);
    return response.data;
  } catch (error) {
    console.error("Error fetching improvement suggestions:", error.response?.data || error.message);
    throw error;
  }
};

export const fetchItemTransactions = async (itemName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/items/${itemName}/transactions`);
    return response.data;
  } catch (error) {
    console.error("Error fetching item transactions:", error.response?.data || error.message);
    throw error;
  }
};

export const fetchItemPeopleTransactions = async (itemName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/items/${itemName}/people/transactions`);
    return response.data;
  } catch (error) {
    console.error("Error fetching item people transactions:", error.response?.data || error.message);
    throw error;
  }
};

export const fetchTransfers = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/people/transfers`);
    return response.data;
  } catch (error) {
    console.error("Error fetching received transfers:", error.response?.data || error.message);
    throw error;
  }
};