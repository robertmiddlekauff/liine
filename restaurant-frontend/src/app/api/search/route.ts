import { NextResponse } from "next/server";

/**
 * Return backend type
 */
export async function POST(req: Request) {
  const { time } = (await req.json())
  try {
    const response = await fetch(`http://fastapi-app:8000/restaurants`, {
      method: "POST",
      body: JSON.stringify({ time }),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(
      (response) => response.json() as Promise<string>
    );

    return NextResponse.json<string>(response);
  } catch (e) {
    return NextResponse.json(
      {
        error: "Error fetching backend",
      },
      { status: 500 }
    );
  }
}
