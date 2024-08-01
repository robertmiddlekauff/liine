
import Link from "next/link";
import styles from "./page.module.css";
import { fetchRestaurants, fetchWelcome } from "./requests";

export const revalidate = 0;

export default async function Home() {
  const welcome = await fetchWelcome()
  const restaurants = await fetchRestaurants()

  return (
    <main className={styles.main}>
      <div className={styles.description}>{welcome}</div>
      <br />
      <Link href="/search"><button>Search</button></Link>
      <div dangerouslySetInnerHTML={{ __html: restaurants.restaurants }} />
    </main>
  );
}
