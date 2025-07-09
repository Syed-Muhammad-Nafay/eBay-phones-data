import asyncio
import random
from bs4 import BeautifulSoup
import nodriver as uc
from curl_cffi import requests
from fake_useragent import UserAgent
from database import initiat_schema, add_a_record

class EbayHumanStealthScraper:
    async def scrape_stealthily(self):
        initiat_schema(table_name='iphones')
        subjects = [
                "iPhone 15 Pro Max 256GB ",
                "iPhone 15 128GB ",
                "iPhone 14 Pro 256GB",
                "iPhone 13 Pro Max 128GB",
                "iPhone 13 128GB",
                "iPhone 12 64GB",
                "iPhone 11 Pro 256GB",
                "iPhone XR 128GB",
                "iPhone SE 3rd Gen 64GB",
                "iPhone 8 64GB"
        ]
        subjects = [y.replace(" ", "+") for y in subjects]
        conditions = ['1000', '1500', '2000', '3000']

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": "__gads=ID=640664b97b6dc241:T=1747643963:RT=1747643963:S=ALNI_Ma2oQoBt5yP29N0yBZHiXzX6eaNbw; __gpi=UID=000010b385b02f28:T=1747643963:RT=1747643963:S=ALNI_MZ5ep6em8l3wZiWx1xGDz0tXJBRMQ; __eoi=ID=2ceebdf764eb44f3:T=1747643963:RT=1747643963:S=AA-Afjae2_Dw19XBKxEjWD61roUm; FCNEC=%5B%5B%22AKsRol-4XiY47VgsYMnafw3XxgX_0EQ9RBKiqm6m0DZwS2ywZrEOm4aW7jDFZvTV1ELl_Uw1zt-CRQXbEqLOvS93wH1DYxHgfMm-23vzGR7E-gyyvzLdocUdNFPvtRyO-bxuhMHSSfp08Jie44me62Ypyvc81Qwh-Q%3D%3D%22%5D%5D",
            "Device-Memory": "8",
            "Downlink": "0.9",
            "Dpr": "1",
            "Ect": "4g",
            "Host": "www.ebay.com",
            "Priority": "u=0, i",
            "Referer": "https://www.bing.com/",
            "Rtt": "250",
            "Sec-Ch-Prefers-Color-Scheme": "dark",
            "Sec-Ch-Prefers-Reduced-Motion": "no-preference",
            "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            "Sec-Ch-Ua-Arch": "x86",
            "Sec-Ch-Ua-Full-Version": "134.0.3124.83",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Model": "",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Platform-Version": "10.0.0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Viewport-Width": "1358"
        }

        ua = UserAgent()
        # Use ProactorEventLoop for Windows to handle subprocesses better
        if asyncio.get_event_loop().is_closed():
            loop = asyncio.ProactorEventLoop()  # Windows-specific event loop
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()

        browser = await uc.start(
            headless=False,  # Set to True for headless mode
            browser_args=[
                f'--window-size={random.choice([1280, 1366, 1440, 1920])},{random.choice([720, 768, 900, 1080])}'
            ]
        )

        try:
            for subject in subjects:
                for condition in conditions:
                    for page in range(1, 4):  
                        url = (
                            f"https://www.ebay.com/sch/i.html?_nkw={subject}"
                            f"&_sacat=0&_from=R40&rt=nc&LH_ItemCondition={condition}&_pgn={page}"
                        )
                        
                        await asyncio.sleep(random.uniform(3.0, 6.0))
                        headers['User-Agent'] = ua.random
                        try:
                            response = requests.get(url, headers=headers, impersonate="edge")
                            response.raise_for_status()
                            html = response.text
                            use_nodriver = False
                        except Exception as e:
                            print(f"⚠️ curl_cffi failed for {url}: {e}. Falling back to nodriver.")
                            tab = await browser.get(url)

                            for _ in range(random.randint(2, 4)):
                                await asyncio.sleep(random.uniform(1.5, 2.5))
                                scroll_position = random.randint(200, 1200)
                                await tab.evaluate(f"window.scrollTo(0, {scroll_position});")

                            await asyncio.sleep(random.uniform(2.0, 4.0))
                            await tab.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                            await asyncio.sleep(random.uniform(2.0, 4.0))

                            html = await tab.content
                            use_nodriver = True

                        soup = BeautifulSoup(html, "html.parser")

                        categorytag = soup.find('ul', class_='srp-refine__category__list')
                        if categorytag:
                            optiontag = [x.text for x in categorytag.find_all('span')]
                            category = next((item for item in optiontag if item.startswith("Selected")), "Unknown")
                        else:
                            category = "Unknown"

                        print(f"\n📦 Category: {category} | Condition Code: {condition} | Page: {page}")

                        divs = soup.find_all("div", class_="s-item__info")
                        for div in divs:
                            titletag = div.find("span", attrs={"role": "heading"})
                            if titletag:
                                title = titletag.text.strip()
                                if "Shop on eBay" in title:
                                    continue

                                conditiontag = div.find("span", class_="SECONDARY_INFO")
                                condition_text = conditiontag.text if conditiontag else "N/A"

                                pricetag = div.find("span", class_="s-item__price")
                                price = pricetag.text if pricetag else "N/A"

                                locationtag = div.find("span", class_="s-item__location s-item__itemLocation")
                                location = locationtag.text if locationtag else "N/A"

                                deliverytag = div.find("span", class_="s-item__shipping s-item__logisticsCost")
                                delivery = deliverytag.text if deliverytag else "N/A"

                                try:
                                    add_a_record(title, condition_text, price, location, delivery, category, table_name='iphones')
                                except Exception as db_e:
                                    print(f"Failed to add record to database: {db_e}")

                        await asyncio.sleep(random.uniform(5.0, 10.0))
                    print(f"⏸️ Finished subject: {subject.replace('+', ' ')}. Pausing before next...")
                    await asyncio.sleep(random.uniform(10.0, 20.0)) 
        finally:
            # Ensure all pending tasks are complete before closing the browser
            await asyncio.sleep(1)  # Small delay to allow tasks to settle
            await browser.stop()
            # Explicitly run pending tasks before closing the loop
            pending = asyncio.all_tasks(loop=loop)
            for task in pending:
                if task is not asyncio.current_task(loop=loop):
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

if __name__ == "__main__":  
    scraper = EbayHumanStealthScraper()
    asyncio.run(scraper.scrape_stealthily())