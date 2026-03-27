import json
import os


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def merge_tests(json1_path: str, json2_path: str, timed_source: int, keep_other_timed: bool = True,
                data1: dict = None, data2: dict = None) -> dict:
    data1 = data1 if data1 is not None else load_json(json1_path)
    data2 = data2 if data2 is not None else load_json(json2_path)

    test1_meta = data1["TEST.0"]
    test2_meta = data2["TEST.0"]

    timed1 = test1_meta["timed"]
    timed2 = test2_meta["timed"]

    # Determine which timed question to keep and which becomes a regular question
    if timed_source == 1:
        chosen_timed = timed1
        demoted_timed = timed2
    else:
        chosen_timed = timed2
        demoted_timed = timed1

    # Collect all question keys from both files (everything except TEST.0)
    all_questions: dict = {}
    for key, value in data1.items():
        if key != "TEST.0":
            all_questions[key] = value
    for key, value in data2.items():
        if key != "TEST.0":
            all_questions[key] = value

    # Build the merged question number list:
    # all question numbers from both tests, excluding the chosen timed question
    questions1 = test1_meta["questions"]
    questions2 = test2_meta["questions"]

    all_question_numbers = []
    # Optionally include the demoted timed question as a regular question
    if keep_other_timed:
        all_question_numbers.append(demoted_timed)
    all_question_numbers.extend(questions1)
    all_question_numbers.extend(questions2)
    # Remove the chosen timed from the regular list (it shouldn't appear there)
    all_question_numbers = [n for n in all_question_numbers if n != chosen_timed]
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for n in all_question_numbers:
        if n not in seen:
            seen.add(n)
            deduped.append(n)
    all_question_numbers = deduped

    title1 = test1_meta.get("title", "Test 1")
    title2 = test2_meta.get("title", "Test 2")
    merged_title = f"{title1} + {title2}"

    merged_test0 = {
        "timed": chosen_timed,
        "count": len(all_question_numbers),
        "questions": all_question_numbers,
        "title": merged_title,
        "useCustomHeader": test1_meta.get("useCustomHeader", False),
        "customHeader": test1_meta.get("customHeader", ""),
        "testtype": test1_meta.get("testtype", "none"),
    }

    merged = {"TEST.0": merged_test0}
    merged.update(all_questions)

    return merged


def prompt_file(label: str) -> tuple[str, dict]:
    """Prompt for a JSON file path, validate it, and return (path, parsed data)."""
    while True:
        path = input(f"{label}: ").strip()
        if not os.path.isfile(path):
            print(f"  File not found: {path!r}. Please try again.")
            continue
        try:
            data = load_json(path)
            if "TEST.0" not in data:
                print(f"  No TEST.0 key found in {path!r}. Is this the right file?")
                continue
            return path, data
        except json.JSONDecodeError as e:
            print(f"  Could not parse JSON: {e}. Please try again.")


def prompt_choice(prompt: str, valid: dict) -> str:
    """Prompt until the user enters a key from `valid`. Returns the matched key."""
    options = "  /  ".join(f"{k} = {v}" for k, v in valid.items())
    while True:
        answer = input(f"{prompt} ({options}): ").strip().lower()
        if answer in valid:
            return answer
        print(f"  Invalid input. Please enter one of: {', '.join(valid)}")


def main():
    print("=== Merge State Tests ===\n")

    json1_path, data1 = prompt_file("Path to first test JSON")
    json2_path, data2 = prompt_file("Path to second test JSON")

    title1 = data1["TEST.0"].get("title", os.path.basename(json1_path))
    title2 = data2["TEST.0"].get("title", os.path.basename(json2_path))

    timed_source = int(prompt_choice(
        "Which test's timed question to use",
        {"1": title1, "2": title2},
    ))

    other_title = title2 if timed_source == 1 else title1
    keep_other_timed = prompt_choice(
        f"Keep '{other_title}' timed question as a regular question",
        {"keep": "include it", "discard": "drop it"},
    ) == "keep"

    merged = merge_tests(json1_path, json2_path, timed_source, keep_other_timed, data1, data2)

    # Derive output filename from the two input filenames
    base1 = os.path.splitext(os.path.basename(json1_path))[0]
    base2 = os.path.splitext(os.path.basename(json2_path))[0]
    out_dir = os.path.dirname(os.path.abspath(json1_path))
    out_path = os.path.join(out_dir, f"{base1} + {base2}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4, ensure_ascii=False)

    timed_q = merged["TEST.0"]["timed"]
    q_count = merged["TEST.0"]["count"]
    other_timed = merged["TEST.0"]["questions"][0] if keep_other_timed else None
    print(f"Merged test written to: {out_path}")
    print(f"  Timed question:         {timed_q}")
    print(f"  Other timed question:   {'kept as Q' + str(other_timed) if keep_other_timed else 'discarded'}")
    print(f"  Regular questions:      {q_count}")


if __name__ == "__main__":
    main()
