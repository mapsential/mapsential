#!/bin/python3

import aiohttp
import asyncio
import datetime
import random

import click


@click.group()
@click.option("-n", "--num", default=10, help="Number of requests to send at the same time")
@click.option("-r", "--reps", default=10, help="Number of times to repeat requests")
@click.option("-d", "--delay", default=1, help="")
@click.option(
    "-o", "--url-order", 
    type=click.Choice(["random", "rnd", "sequential", "seq"]), 
    default="random",
    help="Order in which a single url is chosen (if multiple urls are possible)",
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="Show request responses")
@click.pass_context
def cli(ctx, **kwargs):
    ctx.ensure_object(dict)

    ctx.obj = dict(kwargs)


@cli.command()
@click.pass_context
def rest_api_locations(ctx):
    url_base = "https://mapsential.de/api/filter_locations/"
    urls = [
        f"{url_base}{location_type}" 
        for location_type in [
            "defibrillator", 
            "drinking_fountain", 
            "soup_kitchen", 
            "toilet"
        ]
    ]
    test_urls_by_order(urls, **ctx.obj)


@cli.command()
@click.pass_context
def frontend(ctx):
    kwargs = {k: v for k, v in ctx.obj.items() if k != "url_order"}

    test_urls("https://mapsential.de", **kwargs)


def test_urls_by_order(urls, url_order, **kwargs):
    if url_order in {"random", "rnd"}:
        def urls_gen():
            while True:
                yield random.choice(urls)

        urls_iter = urls_gen()
    elif url_order in {"sequential", "seq"}:
        def urls_gen():
            i = 0
            while True:
                yield urls[i % len(urls)]
        
        urls_iter = urls_gen()
    else:
        raise ValueError(f"Invalid url oder '{url_order}'")

    test_urls(urls_iter, **kwargs)


def test_urls(urls, num, reps, delay, verbose):
    async def func():
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(connect=1000)) as session:
            success_count = 0
            failure_count = 0

            async def handle_url(i, url):
                nonlocal success_count
                nonlocal failure_count

                async with session.get(url) as response:
                    body = await response.text()

                    log_prefix = f"{response.url}: {now}: request {i + 1}"
                    if response.status == 200:
                        print(f"{log_prefix} succeeded :)")
                        if verbose:
                            print(body)
                        success_count += 1
                    else:
                        print(
                            f"{log_prefix} failed with status {response.status} and data:\n{body}"
                        )
                        if verbose:
                            print(body)
                        failure_count += 1

            for _ in range(reps):
                now = datetime.datetime.now()

                if hasattr(urls, "__next__"):
                    urls_ = []
                    for _ in range(num):
                        urls_.append(next(urls))
                else:
                    urls_ = [urls] * num

                await asyncio.gather(*[handle_url(i, url) for i, url in enumerate(urls_)])

                print("-" * 74)
                await asyncio.sleep(delay)

            print(f"{success_count} requests succeeded and {failure_count} requests failed")
            print("=" * 74)

    asyncio.run(func())


async def fetch_urls(urls):
    async with aiohttp.ClientSession() as session:
        async def fetch(url):
            async with session.get(url) as response:
                return response

        return await asyncio.gather(*[fetch(url) for url in urls])


if __name__ == "__main__":
    cli()