import pytest

test_suite = [
    "tests/test_login.py",
    "tests/test_forgot_password.py",
    "tests/test_landing.py",
    "tests/test_newuser.py",
]

def main():
    args = [
        "-v",
        "--headed",
        "--screenshot=only-on-failure",
        "--video=retain-on-failure",
        *test_suite
    ]

    print("\nRunning suite with:", test_suite)
    exit_code = pytest.main(args)
    exit(exit_code)


if __name__ == "__main__":
    main()
