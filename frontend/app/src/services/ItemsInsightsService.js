import axios from "axios";

const BASE_URL = "http://localhost:5000/api/item_insights";

export const fetchTopSellingItems = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/top_selling_items`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching top-selling items:", error);
    throw error;
  }
};

export const fetchMostProfitableItems = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/most_profitable_items`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching most profitable items:", error);
    throw error;
  }
};

export const fetchStoresWithMostSales = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/stores_with_most_sales`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching stores with most sales:", error);
    throw error;
  }
};

export const fetchStoresWithMostRevenue = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/stores_with_most_revenue`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching stores with most revenue:", error);
    throw error;
  }
};

export const fetchMostPromotedItems = async (filters = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/most_promoted_items`, {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching most promoted items:", error);
    throw error;
  }
};

export const fetchTopSellingProductsByAge = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/top_selling_item_by_ages`);
    return response.data;
  } catch (error) {
    console.error("Error fetching top-selling item by ages:", error);
    throw error;
  }
};
