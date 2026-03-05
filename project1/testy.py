# testy.py
# from signal import signal, alarm, SIGALRM

import sys
import time
from copy import deepcopy
import concurrent.futures

# TIMER = False
TIMER = True
# RERAISE = False
RERAISE = True
ALLOWED_TIME = 1

HAS_SIGALRM = False
if TIMER:
    try:
        # SIGALRM is not available on Windows; try import and fall back if missing
        from signal import SIGALRM, alarm, signal
        HAS_SIGALRM = True
    except (ImportError, AttributeError):
        HAS_SIGALRM = False


# format testów
# problems = [ {"arg":arg0, "hint": hint0}, {"arg":arg1, "hint": hint1}, ... ]


def list2str(L):
    s = ""
    for x in L:
        s += str(x) + ", "
    s = s.strip()
    if len(s) > 0:
        s = s[:-1]
    return s


def limit(L, lim=120):
    x = str(L)
    if len(x) < lim:
        return x
    else:
        return x[:lim] + "[za dlugie]..."


class TimeOut(Exception):
    def __init__(self):
        pass


def timeout_handler(signum, frame):
    raise TimeOut()


def run_f_with_timeout(f, args, timeout):
    """Run f(*args) with a timeout. Prefer SIGALRM when available (Unix).
    When SIGALRM isn't available (e.g., on Windows), use a thread-based
    fallback that raises TimeOut when the call doesn't complete in time.
    Note: the thread fallback won't forcibly terminate the executing function,
    but it allows the test runner to continue and report a timeout.
    """
    if HAS_SIGALRM:
        # Use signal alarm (works only on Unix-like systems)
        signal(SIGALRM, timeout_handler)
        alarm(timeout)
        try:
            return f(*args)
        finally:
            alarm(0)
    elif TIMER:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(f, *args)
            try:
                return fut.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                raise TimeOut()
    else:
        return f(*args)


def internal_runtests(printarg, printhint, printsol, check, problems, f):
    passed = 0
    wrong = 0
    timed_out = 0

    total = len(problems)
    total_time = 0

    for i, (name, data) in enumerate(problems.items(), start=1):
        print("-----------------")
        print(f"Test {i} - {name}")
        arg = deepcopy(data["arg"])
        hint = deepcopy(data["hint"])
        printarg(*arg)
        printhint(hint)
        try:
            time_s = time.time()
            sol = run_f_with_timeout(f, arg, ALLOWED_TIME + 1) if TIMER else f(*arg)
            time_e = time.time()

            printsol(sol)
            if check(*arg, hint, sol):
                passed += 1
            else:
                wrong += 1

            time_spent = float(time_e - time_s)
            print(f"Orientacyjny czas: {time_spent:.2f} sek.")
            total_time += time_spent
        except TimeOut:
            print("!!!!!!!! PRZEKROCZONY DOPUSZCZALNY CZAS")
            timed_out += 1
        except KeyboardInterrupt:
            print("Obliczenia przerwane przez operatora")
        except Exception as e:
            print("WYJATEK:", e)
            if RERAISE:
                raise e

    print("-----------------")
    print(
        f"Liczba zaliczonych testów: {passed}/{total} "
        f"(zle: {wrong}, timeout: {timed_out})"
    )
    print(f"Orientacyjny łączny czas : {total_time:.2f} sek.")

    solution_name = sys.argv[0].replace("_", " ").replace(".py", "")

    print(f"{solution_name} {passed} {total} {total_time:.2f}", file=sys.stderr)
