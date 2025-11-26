import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const MORALIS_API_KEY = process.env.MORALIS_API_KEY;

/**
 * 查询地址标签
 * @param {string} address 钱包地址（带 0x 前缀）
 * @param {string} chain   链名，例如 'eth', 'bsc', 'polygon' 等
 */
async function getAddressLabel(address, chain = 'eth') {
  const url = `https://deep-index.moralis.io/api/v2.2/address/${address}/labels?chain=${chain}`;
  
  try {
    const response = await axios.get(url, {
      headers: {
        'accept': 'application/json',
        'X-API-Key': MORALIS_API_KEY
      }
    });

    if (response.data.length === 0) {
      console.log('No label found for this address.');
    } else {
      for (const label of response.data) {
        console.log('--- Label Result ---');
        console.log('Address:  ', address);
        console.log('Entity:   ', label.entity || 'N/A');
        console.log('Type:     ', label.type || 'N/A');
        console.log('Category: ', label.category || 'N/A');
        console.log('Updated:  ', label.last_updated_at);
        console.log('-----------');
      }
    }
  } catch (err) {
    console.error('Error querying Moralis:', err.response?.data || err.message);
  }
}

// 示例调用
const testAddress = '0x00799bbc833D5B168F0410312d2a8fD9e0e3079c';  // Bitfinex 热钱包
getAddressLabel(testAddress, 'eth');

