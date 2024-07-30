"use client";

import styles from "./page.module.css";
import { useEffect, useState } from "react";

export default function Home() {
  const [welcome, setWelcome] = useState<string>(
    "Welcome to the restaurant locator!"
  );
  const [restaurants, setRestaurants] = useState<{ restaurants: string }>(
    { restaurants: "No restaurants found"}
  );
  useEffect(() => {
    const fetchWelcome = async () => {
      try {
        const response = await fetch("/api", { method: "GET" }); // Assuming your API route is /api/stream
        const data = await response.json();
        setWelcome(data);
      } catch (e) {
        console.error(e);
      }
    };
    const fetchRestaurants = async () => {
      try {
        const response = await fetch("/api/restaurants", { method: "GET" }); // Assuming your API route is /api/stream
        const data = await response.json();
        setRestaurants(data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchWelcome().then(() => {}).catch(() => {});
    fetchRestaurants().then(() => {}).catch(() => {});
  });
  return (
    <main className={styles.main}>
      <div className={styles.description}>{welcome}</div>
      <div dangerouslySetInnerHTML={{ __html: restaurants.restaurants }} />
    </main>
  );
}
