import sys
import time

import requests


BASE_URL = "http://127.0.0.1:8000"


def print_result(name, success, response=None):
    status = "PASS" if success else "FAIL"

    print("\n" + "=" * 60)
    print(f"[{status}] {name}")

    if response is not None:
        print(f"Status Code: {response.status_code}")

        try:
            print("Response:")
            print(response.json())
        except ValueError:
            print("Response:")
            print(response.text)


def test_health():
    name = "GET /health"

    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=10,
        )

        success = response.status_code == 200

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_llm_info():
    name = "GET /llm/info"

    try:
        response = requests.get(
            f"{BASE_URL}/llm/info",
            timeout=10,
        )

        success = response.status_code == 200

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_llm_status(expected_loaded=None):
    name = "GET /llm/status"

    try:
        response = requests.get(
            f"{BASE_URL}/llm/status",
            timeout=10,
        )

        success = response.status_code == 200

        if success and expected_loaded is not None:
            data = response.json()
            success = data.get("loaded") == expected_loaded

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_load_model():
    name = "POST /llm/load"

    try:
        print("\nLoading model. This may take some time...")

        response = requests.post(
            f"{BASE_URL}/llm/load",
            timeout=300,
        )

        success = (
            response.status_code == 200
            and response.json().get("success") is True
            and response.json().get("loaded") is True
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_chat():
    name = "POST /chat"

    payload = {
        "message": "Reply with exactly: Local Codex is working",
        "temperature": 0.1,
        "max_tokens": 50,
    }

    try:
        print("\nGenerating AI response...")

        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=300,
        )

        success = (
            response.status_code == 200
            and "response" in response.json()
            and len(response.json()["response"]) > 0
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_chat_stream():
    name = "POST /chat/stream"

    payload = {
        "message": "Say hello in one short sentence.",
        "temperature": 0.1,
        "max_tokens": 50,
    }

    try:
        print("\nStreaming AI response...")

        response = requests.post(
            f"{BASE_URL}/chat/stream",
            json=payload,
            stream=True,
            timeout=300,
        )

        if response.status_code != 200:
            print_result(name, False, response)
            return False

        received_tokens = []
        received_done = False

        for line in response.iter_lines(
            decode_unicode=True
        ):
            if not line:
                continue

            if line.startswith("data: "):
                data = line[6:]

                if data == "[DONE]":
                    received_done = True
                    break

                received_tokens.append(data)
                print(data)

        success = (
            len(received_tokens) > 0
            and received_done
        )

        print("\n" + "=" * 60)
        print(
            f"[{'PASS' if success else 'FAIL'}] {name}"
        )
        print(
            f"Received chunks: {len(received_tokens)}"
        )
        print(f"Received DONE: {received_done}")

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_validation():
    name = "POST /chat - Validation Test"

    payload = {
        "message": "",
        "temperature": 5,
        "max_tokens": -10,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=10,
        )

        success = response.status_code == 422

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def test_unload_model():
    name = "POST /llm/unload"

    try:
        response = requests.post(
            f"{BASE_URL}/llm/unload",
            timeout=60,
        )

        success = (
            response.status_code == 200
            and response.json().get("success") is True
            and response.json().get("loaded") is False
        )

        print_result(name, success, response)

        return success

    except requests.RequestException as error:
        print(f"\n[FAIL] {name}")
        print(error)

        return False


def run_tests():
    print("=" * 60)
    print("LOCAL CODEX - PHASE 1 API TESTS")
    print("=" * 60)

    results = []

    # Basic backend tests
    results.append(test_health())
    results.append(test_llm_info())

    # Initial model status
    results.append(test_llm_status())

    # Load model
    results.append(test_load_model())

    # Verify model loaded
    results.append(
        test_llm_status(expected_loaded=True)
    )

    # Chat tests
    results.append(test_chat())
    results.append(test_chat_stream())

    # Validation test
    results.append(test_validation())

    # Unload model
    results.append(test_unload_model())

    # Verify model unloaded
    results.append(
        test_llm_status(expected_loaded=False)
    )

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\nALL TESTS PASSED! 🎉")
        return 0

    print("\nSOME TESTS FAILED.")
    return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)