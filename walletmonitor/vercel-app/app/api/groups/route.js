import { getAvailableGroups } from '../../lib/database.js';

export async function GET() {
  try {
    const groups = await getAvailableGroups();
    
    return Response.json({
      success: true,
      data: groups
    });
  } catch (error) {
    console.error('Error fetching groups:', error);
    return Response.json(
      { success: false, error: 'Failed to fetch groups' },
      { status: 500 }
    );
  }
} 