from time import perf_counter
from .logger import get_logger
from .extract import extract
from .transform import transform
from .quality import run_quality_checks
from .load import load

log = get_logger()

def run():
    t0 = perf_counter()
    log.info("Pipeline started")

    raw = extract()
    log.info(f"Extract done: {raw}")

    processed = transform(raw)
    log.info(f"Transform done: {processed}")

    run_quality_checks(processed)
    log.info("Quality checks passed")

    n = load(processed)
    log.info(f"Load done: inserted/updated {n} rows")

    log.info(f"Pipeline finished in {perf_counter() - t0:.2f}s")

if __name__ == "__main__":
    run()
