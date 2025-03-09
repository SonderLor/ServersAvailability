import httpx
import asyncio
from prometheus_client import Gauge

http_status = Gauge("server_http_status", "HTTP Status", ["server"])
response_time = Gauge(
    "server_response_time", "Response time in seconds", ["server"]
)


async def check_server(url):
    try:
        async with httpx.AsyncClient() as client:
            start = asyncio.get_event_loop().time()
            response = await client.get(url)
            elapsed = asyncio.get_event_loop().time() - start
            http_status.labels(server=url).set(response.status_code)
            response_time.labels(server=url).set(elapsed)
            return {"url": url, "status": response.status_code}
    except Exception:
        http_status.labels(server=url).set(0)
        response_time.labels(server=url).set(-1)
        return {"url": url, "status": "DOWN"}
