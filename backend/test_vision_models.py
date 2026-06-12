#!/usr/bin/env python3
"""
Vision Model Benchmark for CityPulse Image Classification.

Tests multiple Ollama vision models against sample images and compares:
- Classification accuracy
- Response time per image
- Per-category detection results

Usage:
    uv run python test_vision_models.py <image_path>
    uv run python test_vision_models.py <image_path> --models moondream,llava
    uv run python test_vision_models.py <image_path> --expected "Road Maintenance"
    uv run python test_vision_models.py <image_path> --ollama-url http://localhost:11434
"""

import argparse
import base64
import json
import os
import sys
import time
from typing import Dict, List, Optional

# ── Models to test by default ─────────────────────────────────────

DEFAULT_MODELS = [
    "gemma4:31b-cloud",
    "moondream",
    "llava",
    "minicpm-v",
    "bakllava",
]

# ── Category prompts (same as image_classifier.py) ───────────────

CATEGORIES = [
    "Road Maintenance",
    "Electricity",
    "Water Supply",
    "Waste Management",
    "Public Transportation",
]

DETECT_PROMPTS = {
    "Road Maintenance": (
        "Look at this image. Is there a pothole, cracked road, damaged sidewalk, "
        "broken street light, road debris, or any road/pavement damage? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Electricity": (
        "Look at this image. Is there a downed power line, broken street lamp, "
        "damaged transformer, exposed wire, fallen utility pole, or any electrical hazard? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Water Supply": (
        "Look at this image. Is there a water leak, burst pipe, flooding, "
        "broken hydrant, waterlogging, or any water infrastructure damage? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Waste Management": (
        "Look at this image. Is there a garbage pile, overflowing trash bin, "
        "illegal dumping, scattered litter, or any waste management issue? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Public Transportation": (
        "Look at this image. Is there a damaged bus stop, broken bus shelter, "
        "damaged metro station, broken ticket machine, or any transit infrastructure damage? "
        "Answer YES or NO and briefly describe what you see."
    ),
}


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_yes_no(response: str) -> bool:
    upper = response.upper().strip()
    first_word = upper.split()[0] if upper.split() else ""
    return first_word in ("YES", "YES,", "YES.")


def get_available_models(ollama_url: str) -> List[str]:
    """Fetch list of models pulled into Ollama."""
    import ollama

    client = ollama.Client(host=ollama_url)
    try:
        models = client.list()
        return [m.model for m in models.models]
    except Exception as e:
        print(f"[ERROR] Could not connect to Ollama at {ollama_url}: {e}")
        sys.exit(1)


def test_model(
    model: str,
    image_path: str,
    ollama_url: str,
    expected_category: Optional[str] = None,
) -> Dict:
    """
    Test a single model against an image across all categories.

    Returns:
        Dict with: model, category, confidence, detections, time_seconds, raw_responses
    """
    import ollama

    client = ollama.Client(host=ollama_url)
    img_b64 = image_to_base64(image_path)

    detections = []
    raw_responses = {}
    total_time = 0.0

    for category, prompt in DETECT_PROMPTS.items():
        start = time.time()
        try:
            response = client.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [img_b64],
                    }
                ],
                options={"temperature": 0.1},
            )
            elapsed = time.time() - start
            total_time += elapsed
            text = response["message"]["content"].strip()
            raw_responses[category] = text

            is_detected = parse_yes_no(text)
            if is_detected:
                detections.append({
                    "category": category,
                    "confidence": 0.75,
                    "description": text[:150],
                    "time": round(elapsed, 2),
                })

        except Exception as e:
            elapsed = time.time() - start
            total_time += elapsed
            raw_responses[category] = f"[ERROR] {e}"

    # Determine best category
    if detections:
        best_cat = detections[0]["category"]
        confidence = 0.75
    else:
        best_cat = "Unspecified"
        confidence = 0.0

    # Check if correct (if expected provided)
    correct = None
    if expected_category:
        correct = best_cat.lower() == expected_category.lower()

    return {
        "model": model,
        "category": best_cat,
        "confidence": confidence,
        "detections": detections,
        "time_seconds": round(total_time, 2),
        "correct": correct,
        "raw_responses": raw_responses,
    }


def print_results(results: List[Dict], expected_category: Optional[str] = None):
    """Print a formatted comparison table."""
    print("\n" + "=" * 80)
    print("VISION MODEL BENCHMARK RESULTS")
    print("=" * 80)

    if expected_category:
        print(f"Expected category: {expected_category}")
    print(f"{'=' * 80}\n")

    # Summary table
    header = f"{'Model':<25} {'Detected':<22} {'Time (s)':<10} {'Correct?':<10}"
    print(header)
    print("-" * 70)

    for r in results:
        correct_str = ""
        if r["correct"] is not None:
            correct_str = "PASS" if r["correct"] else "FAIL"

        print(
            f"{r['model']:<25} {r['category']:<22} {r['time_seconds']:<10} {correct_str:<10}"
        )

    print("-" * 70)

    # Detailed results per model
    for r in results:
        print(f"\n{'─' * 70}")
        print(f"Model: {r['model']}")
        print(f"  Result: {r['category']} (confidence: {r['confidence']})")
        print(f"  Time: {r['time_seconds']}s")
        print(f"  Detections: {len(r['detections'])}")

        if r["detections"]:
            for d in r["detections"]:
                print(f"    - {d['category']}: {d['description'][:80]}...")

        print(f"\n  Raw responses:")
        for cat, resp in r["raw_responses"].items():
            # Truncate long responses
            short = resp[:100] + "..." if len(resp) > 100 else resp
            print(f"    {cat}: {short}")

    # Winner
    print(f"\n{'=' * 80}")
    if expected_category:
        correct_results = [r for r in results if r["correct"]]
        if correct_results:
            fastest = min(correct_results, key=lambda x: x["time_seconds"])
            print(f"BEST MODEL: {fastest['model']} (correct + fastest at {fastest['time_seconds']}s)")
        else:
            print("NO MODEL GOT THE CORRECT ANSWER")
    else:
        fastest = min(results, key=lambda x: x["time_seconds"])
        print(f"FASTEST MODEL: {fastest['model']} ({fastest['time_seconds']}s)")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark Ollama vision models for CityPulse image classification"
    )
    parser.add_argument("image", help="Path to test image")
    parser.add_argument(
        "--models",
        default=None,
        help=f"Comma-separated list of models (default: {','.join(DEFAULT_MODELS)})",
    )
    parser.add_argument(
        "--expected",
        default=None,
        help="Expected category for accuracy check (e.g. 'Road Maintenance')",
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Ollama server URL (default: http://localhost:11434)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"[ERROR] Image not found: {args.image}")
        sys.exit(1)

    # Determine models to test
    if args.models:
        models = [m.strip() for m in args.models.split(",")]
    else:
        models = DEFAULT_MODELS

    # Check which models are available
    available = get_available_models(args.ollama_url)
    print(f"Ollama URL: {args.ollama_url}")
    print(f"Available models: {', '.join(available)}")

    to_test = [m for m in models if m in available]
    skipped = [m for m in models if m not in available]

    if skipped:
        print(f"Skipped (not pulled): {', '.join(skipped)}")
        print(f"To pull: docker compose exec ollama ollama pull <model>")

    if not to_test:
        print("[ERROR] No models available to test. Pull at least one.")
        sys.exit(1)

    print(f"Testing: {', '.join(to_test)}")
    print(f"Image: {args.image}")
    print()

    # Run tests
    results = []
    for model in to_test:
        print(f"Testing {model}...")
        result = test_model(model, args.image, args.ollama_url, args.expected)
        results.append(result)
        print(f"  -> {result['category']} ({result['time_seconds']}s)")

    # Output
    if args.json:
        # Strip raw_responses for JSON output
        clean = []
        for r in results:
            c = {k: v for k, v in r.items() if k != "raw_responses"}
            clean.append(c)
        print(json.dumps(clean, indent=2))
    else:
        print_results(results, args.expected)


if __name__ == "__main__":
    main()
