import { NextRequest, NextResponse } from 'next/server';

const API_BASE_URL = 'http://13.233.238.90/docs';

export async function GET(
    request: NextRequest,
    context: { params: Promise<{ taskId: string }> }
  
) {
  try {
    const { taskId } = await context.params;
    
    const response = await fetch(`${API_BASE_URL}/videos/${taskId}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    // Get the video content
    const videoBuffer = await response.arrayBuffer();
    
    // Return the video with proper content type
    return new Response(videoBuffer, {
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `inline; filename="video-${taskId}.mp4"`,
      },
    });
  } catch (error) {
    console.error('Error fetching video:', error);
    return NextResponse.json(
      { error: 'Failed to fetch video' },
      { status: 500 }
    );
  }
}
