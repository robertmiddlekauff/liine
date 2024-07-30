import { NextResponse } from "next/server";

/**
 * Return backend type
 */
export async function GET(req: Request) {
  try {
    const response = await fetch(`http://localhost:8000`).then(
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
