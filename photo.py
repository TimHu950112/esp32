
import aiohttp        
import aiofiles
import asyncio
import time
import async_timeout

devices={1:["192.168.135.197","lost"],2:["192.168.135.229","lost"]}
key_list=list(devices.keys())

async def get_photo(ip,name):
    global devices
    for i in devices:
        devices[i][1]="lost"
    try:
        print(name)
        async with async_timeout.timeout(1):
            async with aiohttp.ClientSession() as session:
                async with session.get("http://"+ip+"/check") as resp:
                    print(resp.headers['Content-Type'])

                    if resp.status == 200:
                        devices[name][1]="alive"
                        print(devices[name][1])
                        if resp.headers['Content-Type']=="image/jpeg":
                            f = await aiofiles.open("output/"+str(name)+".jpeg", mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                        else:
                            pass
                        
    except:
        return ip
                
                
async def main():
    # 建立 Task 列表
    tasks = []
    for i in devices:
        tasks.append(asyncio.create_task(get_photo(devices[i][0],i)))
        # 執行所有 Tasks



    # 輸出結果
    
    try:
        await asyncio.wait(tasks, timeout=0.000001)
    except TimeoutError:
        print('The task was cancelled due to a timeout')
        



# if __name__ == '__main__':
#     start = time.perf_counter() # 開始測量執行時間

#     # 執行協同程序
#     asyncio.run(main())



#     elapsed = time.perf_counter() - start # 計算程式執行時間
#     print("執行時間：%f 秒" % elapsed)

ts=time.monotonic()
while True:
    te=time.monotonic()
    if te-ts>1:
        asyncio.run(main())
        ts=te

