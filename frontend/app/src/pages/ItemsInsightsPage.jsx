import React, { useState, useEffect } from "react";
import {
  fetchTopSellingItems,
  fetchMostProfitableItems,
  fetchStoresWithMostSales,
  fetchStoresWithMostRevenue,
  fetchMostPromotedItems,
  fetchTopSellingProductsByAge,
} from "../services/ItemsInsightsService";
import DataTable from "../components/DataTable";
import BarChart from "../components/BarChart";
import NavigationBar from "../components/NavigationBar";

const ItemInsightsPage = () => {
  // State for all the data
  const [topSellingItems, setTopSellingItems] = useState([]);
  const [mostProfitableItems, setMostProfitableItems] = useState([]);
  const [storesWithMostSales, setStoresWithMostSales] = useState([]);
  const [storesWithMostRevenue, setStoresWithMostRevenue] = useState([]);
  const [mostPromotedItems, setMostPromotedItems] = useState([]);
  const [topSellingProductsByAge, setTopSellingProductsByAge] = useState([]);

  useEffect(() => {
    // Fetch all data concurrently
    const fetchData = async () => {
      try {
        const [
          sellingItems,
          profitableItems,
          salesStores,
          revenueStores,
          promotedItems,
          ageProducts,
        ] = await Promise.all([
          fetchTopSellingItems(),
          fetchMostProfitableItems(),
          fetchStoresWithMostSales(),
          fetchStoresWithMostRevenue(),
          fetchMostPromotedItems(),
          fetchTopSellingProductsByAge(),
        ]);

        setTopSellingItems(sellingItems);
        setMostProfitableItems(profitableItems);
        setStoresWithMostSales(salesStores);
        setStoresWithMostRevenue(revenueStores);
        setMostPromotedItems(promotedItems);
        setTopSellingProductsByAge(ageProducts);
      } catch (error) {
        console.error("Error fetching item insights data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <NavigationBar />
      <h1>Item Insights Dashboard</h1>

      <section>
        <h2>Top-Selling Items</h2>
        <DataTable
          data={topSellingItems}
          columns={[
            { header: "Item Name", accessor: "item_name" },
            { header: "Units Sold", accessor: "total_quantity_sold" },
          ]}
        />
        <BarChart
          labels={topSellingItems.map((item) => item.item_name)}
          dataset={topSellingItems.map((item) => item.total_quantity_sold)}
          title="Top-Selling Items"
        />
      </section>

      <section>
        <h2>Most Profitable Items</h2>
        <DataTable
          data={mostProfitableItems}
          columns={[
            { header: "Item Name", accessor: "item_name" },
            { header: "Profit", accessor: "total_profit" },
          ]}
        />
        <BarChart
          labels={mostProfitableItems.map((item) => item.name)}
          dataset={mostProfitableItems.map((item) => item.total_profit)}
          title="Most Profitable Items"
        />
      </section>

      <section>
        <h2>Stores with Most Sales</h2>
        <DataTable
          data={storesWithMostSales}
          columns={[
            { header: "Store Name", accessor: "store" },
            { header: "Sales Count", accessor: "total_items_sold" },
          ]}
        />
        <BarChart
          labels={storesWithMostSales.map((store) => store.store)}
          dataset={storesWithMostSales.map((store) => store.total_items_sold)}
          title="Stores with Most Sales"
        />
      </section>

      <section>
        <h2>Stores with Most Revenue</h2>
        <DataTable
          data={storesWithMostRevenue}
          columns={[
            { header: "Store Name", accessor: "store" },
            { header: "Revenue", accessor: "total_store_revenue" },
          ]}
        />
        <BarChart
          labels={storesWithMostRevenue.map((store) => store.store)}
          dataset={storesWithMostRevenue.map(
            (store) => store.total_store_revenue
          )}
          title="Stores with Most Revenue"
        />
      </section>

      <section>
        <h2>Most Promoted Items</h2>
        <DataTable
          data={mostPromotedItems}
          columns={[
            { header: "Item Name", accessor: "name" },
            { header: "Promotions", accessor: "promotions" },
          ]}
        />
        <BarChart
          labels={mostPromotedItems.map((item) => item.promotion)}
          dataset={mostPromotedItems.map((item) => item.times_on_promotion)}
          title="Most Promoted Items"
        />
      </section>

      <section>
        <h2>Top-Selling Products by Age</h2>
        <DataTable
          data={topSellingProductsByAge}
          columns={[
            { header: "Age Group", accessor: "age_range" },
            { header: "Product Name", accessor: "item_name" },
            { header: "Units Sold", accessor: "total_quantity_sold" },
          ]}
        />
      </section>
    </div>
  );
};

export default ItemInsightsPage;
