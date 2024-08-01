"use server";

export const fetchWelcome = async () => {
  try {
    const response = await fetch("http://fastapi-app:8000", { method: "GET" }); // Assuming your API route is /api/stream
    const data = await response.json();
    return data;
  } catch (e) {
    console.error(e);
    return "error";
  }
};

export const fetchRestaurants = async (time?: string) => {
  try {
    const options: RequestInit = { method: "POST" };
    if (time) {
      options.body = JSON.stringify({ time: time });
    }
    const response = await fetch("http://fastapi-app:8000/restaurants", options); // Assuming your API route is /api/stream
    const data = await response.json();
    return data;
  } catch (e) {
    console.error(e);
    return { restaurants: "error" };
  }
};
