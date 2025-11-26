import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export async function GET(request) {
  try {
    const query = `
      SELECT DISTINCT 
        tk.symbol as value,
        tk.symbol as label
      FROM tokens tk
      INNER JOIN transactions t ON tk.id = t.token_id
      WHERE tk.symbol IS NOT NULL 
      ORDER BY tk.symbol ASC
    `;

    const client = await pool.connect();
    try {
      const result = await client.query(query);
      //console.log('🔍 Tokens API 返回数据:', result.rows);
      return Response.json({
        success: true,
        data: result.rows
      });
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('Error fetching tokens:', error);
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
} 