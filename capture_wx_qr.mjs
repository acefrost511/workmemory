const BASE_URL = "https://ilinkai.weixin.qq.com";

async function fetchQRCode(apiBaseUrl, botType = "3") {
  const base = apiBaseUrl.endsWith("/") ? apiBaseUrl : `${apiBaseUrl}/`;
  const url = new URL(`ilink/bot/get_bot_qrcode?bot_type=${encodeURIComponent(botType)}`, base);
  console.error("Fetching from:", url.toString());

  const response = await fetch(url.toString(), { headers: { "iLink-App-ClientVersion": "1" } });
  if (!response.ok) {
    const body = await response.text().catch(() => "(unreadable)");
    throw new Error(`HTTP ${response.status}: ${body}`);
  }
  return await response.json();
}

try {
  const result = await fetchQRCode(BASE_URL);
  console.log(result.qrcode_img_content);
  // Also save to file
  const fs = await import('node:fs');
  fs.writeFileSync('/tmp/wx_qr_url.txt', result.qrcode_img_content);
  console.error("QR URL saved to /tmp/wx_qr_url.txt");
} catch(e) {
  console.error("ERROR:", e.message);
  process.exit(1);
}
