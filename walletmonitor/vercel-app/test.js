// test.js (ES module)
import axios from 'axios';
import * as cheerio from 'cheerio';

const url = 'https://farside.co.uk/ethereum-etf-flow-all-data/';

const response = await axios.get(url);
const html = response.data;
const $ = cheerio.load(html);

// 找到对应表格
const table = $('h1:contains("Ethereum ETF Flow – All Data")').nextAll('table').first();

if (!table.length) {
  console.error('未找到目标表格');
  process.exit(1);
}

const headers = [];
table.find('thead tr').first().find('th').each((i, th) => {
  headers.push($(th).text().trim());
});

const rows = [];
table.find('tbody tr').each((i, tr) => {
  const row = {};
  $(tr).find('td').each((j, td) => {
    row[headers[j] || `col${j}`] = $(td).text().trim();
  });
  rows.push(row);
});

console.log(JSON.stringify({ headers, rows }, null, 2));
