#!/usr/bin/env python3
"""
Public-case checker for the UFUG2602 project.

Usage:
    python3 check_public.py solution.py

The checker runs the submitted solution on public_test.txt, writes
student_public_output.txt, and reports which public checks failed.
It uses only public_test.txt and public_expected_output.txt.
"""

import os
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PUBLIC_TEST = SCRIPT_DIR / "public_test.txt"
PUBLIC_EXPECTED = SCRIPT_DIR / "public_expected_output.txt"
STUDENT_OUTPUT = SCRIPT_DIR / "student_public_output.txt"


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def run_student(solution_path):
    cmd = [sys.executable, str(solution_path), str(PUBLIC_TEST), str(STUDENT_OUTPUT)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "Runtime timeout: public test exceeded 60 seconds."

    if result.returncode != 0:
        msg = result.stderr.strip() or result.stdout.strip()
        return False, f"Runtime error: exit code {result.returncode}\n{msg[:2000]}"

    if not STUDENT_OUTPUT.exists():
        return False, f"Output file was not created: {STUDENT_OUTPUT}"

    return True, ""


def parse_sections(lines):
    sections = {"header": []}
    current = "header"
    markers = {
        "Operation A": "A",
        "Operation B": "B",
        "Operation C": "C",
    }

    for line in lines:
        stripped = line.strip()
        found = False
        for marker, name in markers.items():
            if marker in stripped:
                current = name
                sections[current] = []
                found = True
                break
        if not found and stripped:
            sections.setdefault(current, []).append(line)

    return sections


def get_public_huffman_text():
    lines = read_lines(PUBLIC_TEST)
    num_docs = int(lines[0])
    docs = {}
    for i in range(1, num_docs + 1):
        doc_id, _category, content = lines[i].split("|", 2)
        docs[int(doc_id)] = content

    huffman_id = None
    for line in lines[num_docs + 1:]:
        line = line.strip()
        if line.startswith("HUFFMAN "):
            huffman_id = int(line.split()[1])
            break

    return docs.get(huffman_id, "")


def parse_huffman_codes(lines):
    codes = {}
    ratio = verified = orig_len = enc_len = None

    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("Compression Ratio:"):
            match = re.search(r"([\d.]+)%", line)
            if match:
                ratio = float(match.group(1))
        elif line.startswith("Decompression Verified:"):
            verified = "True" in line
        elif line.startswith("Original Length:"):
            match = re.search(r"(\d+) characters", line)
            if match:
                orig_len = int(match.group(1))
        elif line.startswith("Encoded Length:"):
            match = re.search(r"(\d+) bits", line)
            if match:
                enc_len = int(match.group(1))
        elif ":" in line and "=" not in line and "Code Table" not in line:
            parts = raw_line.split(":", 1)
            if len(parts) != 2:
                continue
            ch = parts[0].strip()
            code = parts[1].strip()
            if not code or any(bit not in "01" for bit in code):
                continue
            if ch.startswith("'") and ch.endswith("'"):
                ch = ch[1:-1]
            if ch == "" and len(parts[0]) > 0:
                ch = " "
            if len(ch) <= 2:
                codes[ch] = code

    return codes, ratio, verified, orig_len, enc_len


def check_huffman(lines, original_text):
    codes, ratio, verified, orig_len, enc_len = parse_huffman_codes(lines)
    checks = []

    prefix_free = bool(codes)
    values = list(codes.values())
    for i in range(len(values)):
        for j in range(len(values)):
            if i != j and values[j].startswith(values[i]):
                prefix_free = False
                break
        if not prefix_free:
            break
    checks.append(("valid prefix code", prefix_free))

    covered = bool(original_text) and set(original_text) <= set(codes.keys())
    checks.append(("all original characters covered", covered))

    ratio_ok = False
    if orig_len and orig_len == len(original_text) and enc_len and ratio is not None:
        expected_ratio = enc_len / (orig_len * 8) * 100
        ratio_ok = abs(ratio - expected_ratio) < 0.1
    checks.append(("lengths and compression ratio correct", ratio_ok))

    checks.append(("decompression verified", bool(verified)))
    return checks


def parse_topk(lines):
    result = []
    for line in lines:
        match = re.match(r"\s*(\d+)\.\s*(\w+):\s*(\d+)", line)
        if match:
            result.append((int(match.group(1)), match.group(2), int(match.group(3))))
    return result


def check_topk(student_lines, expected_lines):
    student = parse_topk(student_lines)
    expected = parse_topk(expected_lines)
    failures = []

    for i, expected_entry in enumerate(expected):
        if i >= len(student):
            failures.append((expected_entry[0], expected_entry, None))
            continue
        if student[i] != expected_entry:
            failures.append((expected_entry[0], expected_entry, student[i]))

    if len(student) > len(expected):
        for entry in student[len(expected):]:
            failures.append((entry[0], None, entry))

    return len(expected), failures


def group_kmp_by_pattern(lines):
    groups = {}
    current = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Pattern: "):
            current = stripped
            groups[current] = [stripped]
        elif current is not None:
            groups[current].append(stripped)

    return groups


def compare_line_lists(student_lines, expected_lines):
    failures = []
    total = max(len(student_lines), len(expected_lines))
    for i in range(total):
        expected = expected_lines[i] if i < len(expected_lines) else "<NO EXPECTED LINE>"
        student = student_lines[i] if i < len(student_lines) else "<MISSING>"
        if student != expected:
            failures.append((i + 1, expected, student))
    return failures


def check_kmp(student_lines, expected_lines):
    student_groups = group_kmp_by_pattern(student_lines)
    expected_groups = group_kmp_by_pattern(expected_lines)
    results = []

    for pattern, expected_group in expected_groups.items():
        student_group = student_groups.get(pattern)
        if student_group is None:
            results.append((pattern, len(expected_group), [(1, expected_group[0], "<MISSING PATTERN>")]))
            continue
        failures = compare_line_lists(student_group, expected_group)
        results.append((pattern, len(expected_group), failures))

    extra_patterns = [p for p in student_groups if p not in expected_groups]
    for pattern in extra_patterns:
        results.append((pattern, 0, [(1, "<NO EXPECTED PATTERN>", pattern)]))

    return results


def print_huffman_report(checks):
    print("\nOperation A: Huffman")
    passed = 0
    for name, ok in checks:
        if ok:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
    return passed, len(checks)


def print_topk_report(total, failures):
    print("\nOperation B: Top-K")
    passed = total - sum(1 for _rank, expected, _student in failures if expected is not None)
    if not failures:
        print(f"  [PASS] all {total} ranked entries match")
        return total, total

    print(f"  [FAIL] {len(failures)} mismatch(es)")
    for rank, expected, student in failures:
        if expected is None:
            print(f"    Extra rank {rank}: got {student[1]}:{student[2]}")
        elif student is None:
            print(f"    Rank {rank}: expected {expected[1]}:{expected[2]}, got <MISSING>")
        else:
            print(f"    Rank {rank}: expected {expected[1]}:{expected[2]}, got {student[1]}:{student[2]}")
    return max(passed, 0), total


def print_kmp_report(results):
    print("\nOperation C: KMP Pattern Search")
    passed = 0
    total = 0

    for pattern, _expected_lines, failures in results:
        total += 1
        if not failures:
            passed += 1
            print(f"  [PASS] {pattern}")
            continue

        print(f"  [FAIL] {pattern}")
        for line_no, expected, student in failures[:5]:
            print(f"    Line {line_no}:")
            print(f"      expected: {expected}")
            print(f"      got:      {student}")
        if len(failures) > 5:
            print(f"    ... {len(failures) - 5} more mismatch(es)")

    return passed, total


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_public.py solution.py")
        return 2

    solution_path = Path(sys.argv[1]).expanduser().resolve()
    if not solution_path.exists():
        print(f"Solution file not found: {solution_path}")
        return 2

    ok, error = run_student(solution_path)
    if not ok:
        print(error)
        return 1

    student_lines = read_lines(STUDENT_OUTPUT)
    expected_lines = read_lines(PUBLIC_EXPECTED)
    student_sections = parse_sections(student_lines)
    expected_sections = parse_sections(expected_lines)

    print("Public Test Checker")
    print(f"Solution: {solution_path}")
    print(f"Output:   {STUDENT_OUTPUT}")

    total_passed = 0
    total_checks = 0

    a_checks = check_huffman(student_sections.get("A", []), get_public_huffman_text())
    passed, total = print_huffman_report(a_checks)
    total_passed += passed
    total_checks += total

    b_total, b_failures = check_topk(student_sections.get("B", []), expected_sections.get("B", []))
    passed, total = print_topk_report(b_total, b_failures)
    total_passed += passed
    total_checks += total

    c_results = check_kmp(student_sections.get("C", []), expected_sections.get("C", []))
    passed, total = print_kmp_report(c_results)
    total_passed += passed
    total_checks += total

    print("\nSummary")
    print(f"  Passed {total_passed}/{total_checks} public checks")

    if total_passed == total_checks:
        print("  Result: PASS")
        return 0

    print("  Result: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
