import React, { useState, useEffect } from "react";
import {
  fetchCitiesWithMostClients,
  fetchClientsWithMostPurchases,
  fetchClientsWithMostReceivedFunds,
  fetchClientsWithMostTransferredFunds,
  fetchCountriesWithMostUsers,
  fetchMostRecurringClients,
} from "../services/ClientInsightsService";
import DataTable from "../components/DataTable";
import BarChart from "../components/BarChart";
import NavigationBar from "../components/NavigationBar";

const ClientInsightsPage = () => {
  // State for all the data
  const [mostRecurringClients, setMostRecurringClients] = useState([]);
  const [clientsWithMostPurchases, setClientsWithMostPurchases] = useState([]);
  const [clientsWithMostTransferredFunds, setClientsWithMostTransferredFunds] =
    useState([]);
  const [clientsWithMostReceivedFunds, setClientsWithMostReceivedFunds] =
    useState([]);
  const [citiesWithMostClients, setCitiesWithMostClients] = useState([]);
  const [countriesWithMostUsers, setCountriesWithMostUsers] = useState([]);

  useEffect(() => {
    // Fetch all data concurrently
    const fetchData = async () => {
      try {
        const [recurring, purchases, transferred, received, cities, countries] =
          await Promise.all([
            fetchMostRecurringClients({ limit: 15 }),
            fetchClientsWithMostPurchases({ limit: 15 }),
            fetchClientsWithMostTransferredFunds({ limit: 15 }),
            fetchClientsWithMostReceivedFunds({ limit: 15 }),
            fetchCitiesWithMostClients({ limit: 15 }),
            fetchCountriesWithMostUsers({ limit: 15 }),
          ]);

        setMostRecurringClients(recurring);
        setClientsWithMostPurchases(purchases);
        setClientsWithMostTransferredFunds(transferred);
        setClientsWithMostReceivedFunds(received);
        setCitiesWithMostClients(cities);
        setCountriesWithMostUsers(countries);

        console.log(recurring);
        console.log(purchases);
        console.log(transferred);
        console.log(received);
        console.log(cities);
        console.log(countries);
      } catch (error) {
        console.error("Error fetching client insights data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <NavigationBar />
      <h1>Client Insights Dashboard</h1>

      <section>
        <h2>Most Recurring Clients</h2>
        <DataTable
          data={mostRecurringClients}
          columns={[
            { header: "Client Name", accessor: "first_name" },
            { header: "Recurring Count", accessor: "total_purchases_done" },
          ]}
        />
        <BarChart
          labels={mostRecurringClients.map((client) => client.first_name)}
          dataset={mostRecurringClients.map(
            (client) => client.total_purchases_done
          )}
          title="Most Recurring Clients"
        />
      </section>

      {/* Clients with Most Purchases */}
      <section>
        <h2>Clients with Most Purchases</h2>
        <DataTable
          data={clientsWithMostPurchases}
          columns={[
            { header: "Client Name", accessor: "first_name" },
            { header: "Purchase Count", accessor: "total_items_purchased" },
          ]}
        />
        <BarChart
          labels={clientsWithMostPurchases.map((client) => client.first_name)}
          dataset={clientsWithMostPurchases.map(
            (client) => client.total_items_purchased
          )}
          title="Clients with Most Purchases"
        />
      </section>

      {/* Clients with Most Transferred Funds */}
      <section>
        <h2>Clients with Most Transferred Funds</h2>
        <DataTable
          data={clientsWithMostTransferredFunds}
          columns={[
            { header: "Client Name", accessor: "first_name" },
            {
              header: "Amount Transferred",
              accessor: "total_funds_transferred",
            },
          ]}
        />
      </section>

      {/* Clients with Most Received Funds */}
      <section>
        <h2>Clients with Most Received Funds</h2>
        <DataTable
          data={clientsWithMostReceivedFunds}
          columns={[
            { header: "Client Name", accessor: "first_name" },
            { header: "Amount Received", accessor: "total_funds_received" },
          ]}
        />
      </section>

      {/* Cities with Most Clients */}
      <section>
        <h2>Cities with Most Clients</h2>
        <DataTable
          data={citiesWithMostClients}
          columns={[
            { header: "City Name", accessor: "city" },
            { header: "Client Count", accessor: "total_clients_in_city" },
          ]}
        />
      </section>

      {/* Countries with Most Users */}
      <section>
        <h2>Countries with Most Users</h2>
        <DataTable
          data={countriesWithMostUsers}
          columns={[
            { header: "Country Name", accessor: "country" },
            { header: "User Count", accessor: "total_users_in_country" },
          ]}
        />
      </section>
    </div>
  );
};

export default ClientInsightsPage;
