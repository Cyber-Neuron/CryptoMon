// decrypt-coinglass.js
import CryptoJS from 'crypto-js';
import pako      from 'pako';

/**
 * core  ——   与源站里完全同名、同流程的 Yt()。
 * @param {string} cipherBase64  ——  AES-ECB/PKCS7 + Base64 的密文
 * @param {string} keyStr        ——  16 字节 UTF-8 明文密钥
 * @returns {string}             ——  解出的 UTF-8 字符串（去掉两端引号）
 */
export function Yt(cipherBase64, keyStr) {
  // ① AES-ECB 解密得到 WordArray
  const wordArr = CryptoJS.AES.decrypt(
    cipherBase64,
    CryptoJS.enc.Utf8.parse(keyStr),
    { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 }
  );

  // ② WordArray → 16 进制字符串
  const hex = wordArr.toString(CryptoJS.enc.Hex);

  // ③ hex → Uint8Array → raw-inflate
  const bytes = Uint8Array.from(
    hex.match(/[\da-f]{2}/gi).map(h => parseInt(h, 16))
  );
  const inflated = pako.inflate(bytes, { to: 'string' });

  // ④ URI 解码（escape 与 decodeURIComponent）
  let plain = decodeURIComponent(escape(inflated));

  // ⑤ 去掉可能的首末引号
  if (plain.startsWith('"') && plain.endsWith('"')) {
    plain = plain.slice(1, -1);
  }
  return plain;
}

/**
 * 生成接口专属首把钥匙 key_api（16 字节）。
 * 与服务端保持一致：base64("coinglass"+path+"coinglass").substr(0,16)
 */
export function makeApiKey(apiPath) {
  const b64 = Buffer.from(`coinglass${apiPath}coinglass`).toString('base64');
  return b64.slice(0, 16);
}

/**
 * 完整解密 —— 传入 axios 响应对象即可拿到真正业务数据
 */
export function decryptCoinglassResponse(resp) {
  console.log(resp)
  if (!resp.headers?.user || !resp.data?.data) {
    throw new Error('response 缺少所需字段');
  }
  // ① 先用 key_api 解 headers.user → 得到二把钥匙 key2
  const keyApi = makeApiKey(resp.config.url.replace(resp.config.baseURL, ''));
  const key2   = Yt(resp.headers.user, keyApi);

  // ② 再用 key2 解 body.data.data
  const jsonStr = Yt(resp.data.data, key2);
  // console.log(jsonStr)
  return JSON.parse(jsonStr);
}

/* -------------------------------------------
 * demo
 * -----------------------------------------*/
// (假设 raw 是你抓到的 axios response)
async function demo(raw) {
  try {
    const real = decryptCoinglassResponse(raw);
    console.log(real);
  } catch (err) {
    console.error('解密失败:', err);
  }
}

export default demo;
