import fetch from 'node-fetch';
import { decryptCoinglassResponse } from './decrypt-coinglass.js';
import { SocksProxyAgent } from 'socks-proxy-agent';
import fs from 'fs';

// 生成随机Cache-Ts（13位时间戳+3位随机数）
function randomCacheTs() {
  return Date.now().toString() + Math.floor(Math.random() * 1000).toString().padStart(3, '0');
}
// 生成随机Sec-Ch-Ua-Platform，并返回操作系统名
function randomPlatform() {
  const platforms = [
    { platform: '"macOS"', os: 'Mac OS X' },
    { platform: '"Windows"', os: 'Windows NT 10.0' },
    { platform: '"Linux"', os: 'X11; Linux x86_64' },
    // { platform: '"Android"', os: 'Android 10' },
    // { platform: '"iOS"', os: 'iPhone; CPU iPhone OS 14_0 like Mac OS X' }
  ];
  return platforms[Math.floor(Math.random() * platforms.length)];
}
// 生成随机User-Agent，操作系统信息通过参数传递
function randomUserAgent(osInfo) {
  const chromeVer = Math.floor(Math.random() * 30) + 110;
  const safariVer = Math.floor(Math.random() * 100) + 500;
  let osStr = '';
  // 根据不同平台拼接User-Agent的操作系统部分
  if (osInfo.platform === '"macOS"') {
    const macVer = `${10 + Math.floor(Math.random() * 5)}_${15 + Math.floor(Math.random() * 5)}_${7 + Math.floor(Math.random() * 5)}`;
    osStr = `Macintosh; Intel Mac OS X ${macVer}`;
  } else if (osInfo.platform === '"Windows"') {
    osStr = `Windows NT 10.0; Win64; x64`;
  } else if (osInfo.platform === '"Linux"') {
    osStr = `X11; Linux x86_64`;
  } 
  // else if (osInfo.platform === '"Android"') {
  //   osStr = `Linux; Android 10; Pixel 5`;
  // } else if (osInfo.platform === '"iOS"') {
  //   osStr = `iPhone; CPU iPhone OS 14_0 like Mac OS X`;
  // }
  return `Mozilla/5.0 (${osStr}) AppleWebKit/${safariVer}.36 (KHTML, like Gecko) Chrome/${chromeVer}.0.0.0 Mobile Safari/${safariVer}.36`;
}

// 随机平台和操作系统
const osInfo = randomPlatform();

// 伪造请求头，部分字段用随机内容
const headers = {
  'Accept': 'application/json',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Accept-Language': 'en',
  'Cache-Ts': randomCacheTs(),
  'Encryption': 'true',
  'Language': 'en',
  'Origin': 'https://www.coinglass.com',
  'Priority': 'u=1, i',
  'Referer': 'https://www.coinglass.com/',
  'Sec-Ch-Ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
  'Sec-Ch-Ua-Mobile': '?0',
  'Sec-Ch-Ua-Platform': osInfo.platform,
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': randomUserAgent(osInfo),
};

// Tor代理地址
const proxy = 'socks5h://127.0.0.1:9050';
const agent = new SocksProxyAgent(proxy);

// 请求的URL
const url = 'https://capi.coinglass.com/api/marketHistory?pageNum=1&pageSize=50';
// const option_Url = 'https://capi.coinglass.com/api/option/v2/chart?symbol=ETH&ex=Binance&type=Strike&subtype=250613&currency=USD';
// const url = option_Url;
// 主函数
async function main() {
  // 通过Tor代理发起请求
  console.log('请求的URL:', url);
  console.log('请求的头:', headers); 
  console.log("Agent:", agent);
  // return;
  const resp = await fetch(url, {
    method: 'GET',
    headers,
    agent,
  });
  // 解析json
  const data = await resp.json();
  // 构造解密需要的resp对象
  const fakeResp = {
    headers: { user: resp.headers.get('user') },
    config: { url: '/api/marketHistory', baseURL: 'https://capi.coinglass.com' },
    data: { data: data.data }
  };
  // 解密并输出详细内容
  const result = decryptCoinglassResponse(fakeResp);
  // 写入到result.json文件
  fs.writeFileSync('result.json', JSON.stringify(result, null, 2), 'utf-8');
  console.log('解密结果已写入 result.json');
}

main(); 