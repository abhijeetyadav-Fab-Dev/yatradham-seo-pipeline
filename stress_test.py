"""High-Concurrency Multi-Threaded Stress Test Suite for Yatradham SEO Pipeline."""
import sys
import os
import io

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import time
import json
import random
import concurrent.futures
import threading

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models import PackageInput, SEOOutput, SectionedContent
from database import init_db, save_output, get_output, list_outputs, update_output, bulk_update_status, delete_output, get_stats
from llm_client import LLMClient
import main

# Metrics Collector
metrics_lock = threading.Lock()
metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "latencies": [],
    "errors_by_type": {},
    "db_ops": 0,
    "humanize_ops": 0,
    "detect_ops": 0,
    "generation_ops": 0,
    "export_ops": 0
}

def record_metric(op_type: str, success: bool, latency: float, err: str = None):
    with metrics_lock:
        metrics["total_requests"] += 1
        if success:
            metrics["successful_requests"] += 1
        else:
            metrics["failed_requests"] += 1
            metrics["errors_by_type"][err] = metrics["errors_by_type"].get(err, 0) + 1
        metrics["latencies"].append(latency)
        if op_type == "db":
            metrics["db_ops"] += 1
        elif op_type == "humanize":
            metrics["humanize_ops"] += 1
        elif op_type == "detect":
            metrics["detect_ops"] += 1
        elif op_type == "generation":
            metrics["generation_ops"] += 1
        elif op_type == "export":
            metrics["export_ops"] += 1

def worker_db_stress(worker_id: int, iterations: int = 15):
    """Stress test concurrent database writes, reads, status updates, and deletions."""
    for i in range(iterations):
        t0 = time.time()
        try:
            pkg = PackageInput(
                url=f"https://travel.yatradham.org/stress-package-{worker_id}-{i}",
                name=f"Stress Test Package {worker_id}-{i}",
                cost=f"₹{random.randint(1000, 10000)}",
                duration=f"{random.randint(1, 10)} Days",
                destination="Vrindavan",
                accommodation="Dharamshala",
                food="Sattvic"
            )
            out = SEOOutput(
                package_input=pkg,
                primary_keyword=f"Vrindavan Tour {worker_id}-{i}",
                title_tag=f"Vrindavan Tour {worker_id}-{i} | Yatradham",
                meta_description="A stress test package.",
                sections=SectionedContent(package_overview="Stress overview"),
                qa_score=random.randint(80, 100),
                status=random.choice(["pending", "approved", "rejected"])
            )
            
            # Save
            row_id = save_output(out)
            
            # Read
            fetched = get_output(row_id)
            assert fetched is not None
            
            # Update
            bulk_update_status([row_id], "approved")
            
            # List
            _ = list_outputs(limit=10)
            
            # Delete
            delete_output(row_id)
            
            record_metric("db", True, time.time() - t0)
        except Exception as e:
            record_metric("db", False, time.time() - t0, f"DB Error: {str(e)}")

def worker_detector_stress(worker_id: int, iterations: int = 10):
    """Stress test AI Detector endpoint concurrently."""
    sample_texts = [
        "Rishikesh is nestled in the foothills of the Himalayas. Moreover, it serves as a beacon of spirituality.",
        "When you arrive at Haridwar station, take an auto directly to Ram Jhula. Book your ashram 2 weeks early.",
        "Yoga Nidra allows the nervous system to transition from fight-or-flight to deep parasympathetic repair.",
        "Yatradham.Org offers transparent dharamshala bookings with zero hidden checkout fees across India."
    ]
    for i in range(iterations):
        t0 = time.time()
        try:
            text = random.choice(sample_texts) + f" (Worker {worker_id}-{i})"
            res = main.query_undetectable_detector(text)
            assert "score" in res
            record_metric("detect", True, time.time() - t0)
        except Exception as e:
            record_metric("detect", False, time.time() - t0, f"Detector Error: {str(e)}")

def worker_humanizer_stress(worker_id: int, iterations: int = 5):
    """Stress test multi-threaded parallel markdown humanizer."""
    text_sample = f"""## Section 1: Sacred Journey {worker_id}
Rishikesh is nestled in the foothills of the Himalayas. Moreover, it serves as a beacon of spirituality and a tapestry of yoga.

## Section 2: Essential Logistics
Flights to Dehradun cost ₹4,000 to ₹7,000 one-way. Furthermore, Yatradham.Org provides verified dharamshalas starting at ₹600.

## Section 3: Daily Routine
Wake up at 5:30 AM for morning Ganga Aarti and mindful walking meditation along the ghats."""

    for i in range(iterations):
        t0 = time.time()
        try:
            humanized = main.humanize_markdown_content(text_sample)
            assert len(humanized) > 50
            record_metric("humanize", True, time.time() - t0)
        except Exception as e:
            record_metric("humanize", False, time.time() - t0, f"Humanizer Error: {str(e)}")

def worker_export_stress(worker_id: int, iterations: int = 10):
    """Stress test CSV export streaming and stats aggregation."""
    for i in range(iterations):
        t0 = time.time()
        try:
            # Stats
            _ = get_stats()
            # CSV export response
            res = main.export_csv(status=None)
            assert res.status_code == 200 or res.status_code == 404
            record_metric("export", True, time.time() - t0)
        except Exception as e:
            record_metric("export", False, time.time() - t0, f"Export Error: {str(e)}")

def run_stress_test(concurrency: int = 15):
    print("=" * 80)
    print(f"🔥 STARTING INTENSE SYSTEM STRESS TEST (Concurrency: {concurrency} Workers)")
    print("=" * 80)

    init_db()
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency * 4) as executor:
        futures = []
        
        # Launch DB Stress Workers
        for w in range(concurrency):
            futures.append(executor.submit(worker_db_stress, w, 12))
            
        # Launch AI Detector Stress Workers
        for w in range(concurrency):
            futures.append(executor.submit(worker_detector_stress, w, 8))
            
        # Launch Humanizer Stress Workers
        for w in range(concurrency):
            futures.append(executor.submit(worker_humanizer_stress, w, 3))
            
        # Launch Export / Stats Stress Workers
        for w in range(concurrency):
            futures.append(executor.submit(worker_export_stress, w, 10))

        # Wait for all workers to complete
        concurrent.futures.wait(futures)

    total_duration = time.time() - start_time
    latencies = metrics["latencies"]
    latencies.sort()
    
    p50 = latencies[int(len(latencies) * 0.50)] if latencies else 0
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
    p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0
    avg_lat = sum(latencies) / len(latencies) if latencies else 0
    throughput = metrics["total_requests"] / total_duration if total_duration > 0 else 0

    print("\n" + "=" * 80)
    print("📊 STRESS TEST RESULTS & PERFORMANCE BENCHMARKS")
    print("=" * 80)
    print(f"Total Requests Executed:    {metrics['total_requests']}")
    print(f"Successful Requests:        {metrics['successful_requests']} ({metrics['successful_requests']/metrics['total_requests']*100:.1f}%)")
    print(f"Failed Requests:            {metrics['failed_requests']}")
    print(f"Total Test Duration:        {total_duration:.2f} seconds")
    print(f"System Throughput:          {throughput:.2f} req/sec")
    print(f"Latency Avg:                {avg_lat*1000:.1f} ms")
    print(f"Latency P50:                {p50*1000:.1f} ms")
    print(f"Latency P95:                {p95*1000:.1f} ms")
    print(f"Latency P99:                {p99*1000:.1f} ms")
    print("\nOperations Executed:")
    print(f"  - Database CRUD Ops:      {metrics['db_ops']}")
    print(f"  - AI Detection Calls:     {metrics['detect_ops']}")
    print(f"  - Humanizer Rewrites:     {metrics['humanize_ops']}")
    print(f"  - Export & Stats Calls:   {metrics['export_ops']}")
    
    if metrics["errors_by_type"]:
        print("\n⚠️ Error Breakdown:")
        for err, count in metrics["errors_by_type"].items():
            print(f"  - {err}: {count}")
    else:
        print("\n✅ Zero Errors Encountered Under Heavy Load!")
    print("=" * 80)

if __name__ == "__main__":
    run_stress_test(concurrency=12)
