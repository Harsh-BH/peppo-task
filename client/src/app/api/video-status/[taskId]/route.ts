import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = "http://localhost:8000/api";

// ✅ Correct function signature for Next.js 15
export async function GET(
  request: NextRequest,
  context: { params: Promise<{ taskId: string }> }
) {
  try {
    // ✅ Await the params Promise
    const { taskId } = await context.params;

    const response = await fetch(`${API_BASE_URL}/video-status/${taskId}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error checking video status:", error);
    return NextResponse.json(
      { error: "Failed to check video status" },
      { status: 500 }
    );
  }
}
