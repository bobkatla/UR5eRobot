import asyncio as aso
import pandas as pd

async def count():
    print("One")
    await aso.sleep(0.0000000000001)
    print("Two")

async def main():
    await aso.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    aso.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} excecuted in {elapsed: 0.2f} seconds.")