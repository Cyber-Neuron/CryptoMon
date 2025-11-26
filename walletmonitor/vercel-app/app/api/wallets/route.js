import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const groupName = searchParams.get('groupName');

    let query = `
      SELECT 
        id,
        address,
        friendly_name,
        grp_type,
        grp_name,
        created_at,
        updated_at
      FROM wallets
      WHERE grp_type = 'Hot'
    `;

    const params = [];
    let paramIndex = 1;

    if (groupName) {
      query += ` AND grp_name = $${paramIndex}`;
      params.push(groupName);
      paramIndex++;
    }

    query += ` ORDER BY friendly_name ASC, address ASC`;

    const client = await pool.connect();
    try {
      const result = await client.query(query, params);
      return Response.json({
        success: true,
        data: result.rows
      });
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('Error fetching wallets:', error);
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
} 