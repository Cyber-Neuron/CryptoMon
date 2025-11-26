import { SocksProxyAgent } from 'socks-proxy-agent';

// Tor代理配置
const proxy = 'socks5h://127.0.0.1:9050';
const agent = new SocksProxyAgent(proxy);

// 生成随机User-Agent
function randomUserAgent() {
  const chromeVer = Math.floor(Math.random() * 30) + 110;
  const safariVer = Math.floor(Math.random() * 100) + 500;
  const macVer = `${10 + Math.floor(Math.random() * 5)}_${15 + Math.floor(Math.random() * 5)}_${7 + Math.floor(Math.random() * 5)}`;
  return `Mozilla/5.0 (Macintosh; Intel Mac OS X ${macVer}) AppleWebKit/${safariVer}.36 (KHTML, like Gecko) Chrome/${chromeVer}.0.0.0 Safari/${safariVer}.36`;
}

// 获取默认请求头
function getDefaultHeaders() {
  return {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': randomUserAgent(),
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0'
  };
}

// 获取代理配置
function getProxyConfig() {
  return {
    headers: getDefaultHeaders(),
    httpsAgent: agent,
    timeout: 30000,
    maxRedirects: 5
  };
}

export {
  getProxyConfig,
  getDefaultHeaders,
  randomUserAgent,
  agent
}; 