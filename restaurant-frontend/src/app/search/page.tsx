"use client";
import { useState } from "react";
import { fetchRestaurants } from "../requests";

export default function Home() {
  const [text, setText] = useState("");
  const [results, setResults] = useState<string>("No results");
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value);
  };
  return (
    <div>
      <h1>Search</h1>
      <p>
        Search for restaurants in a format like this please: "2024-07-30 22:00"
      </p>
      <input
        type="text"
        placeholder="Search..."
        onChange={onChange}
        value={text}
      />
      <button
        onClick={async () => {
          const filteredRestaurants = await fetch("/api/search", {
            method: "POST",
            body: JSON.stringify({ time: text }),
          }).then((response) => response.json());
          setResults(
            filteredRestaurants.restaurants.length > 0
              ? filteredRestaurants.restaurants.join("<br>")
              : "No restaurants found."
          );
        }}
      >
        Search
      </button>
      <div dangerouslySetInnerHTML={{ __html: results }} />
    </div>
  );
}
