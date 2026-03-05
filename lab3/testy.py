import os
import time
from dimacs import loadDirectedWeightedGraph

def run_all_tests(lab_function, folder="lab3/graphs-lab3"):
    """
    Uruchamia testy dla wszystkich grafów w folderze.
    lab_function – funkcja rozwiązująca, np. lab0(V, L)
    """
    files = os.listdir(folder)
    passed = 0
    total = 0
    print("=== TESTY AUTOMATYCZNE ===\n")

    for filename in files:
        path = os.path.join(folder, filename)
        if not os.path.isfile(path):
            continue
        total += 1

        # --- odczyt oczekiwanego wyniku z pierwszej linii ---
        expected = None
        with open(path) as f:
            first_line = f.readline().strip()
            if first_line.startswith("c solution"):
                try:
                    expected = int(first_line.split("=")[1])
                except:
                    pass

        # --- test ---
        try:
            V, L = loadDirectedWeightedGraph(path)
            start = time.time()
            result = lab_function(V, L)
            end = time.time()
            ok = (expected is None) or (result == expected)

            status = "✅" if ok else "❌"
            print(f"{status} {filename}: wynik={result}, oczekiwany={expected}, czas={end-start:.4f}s")

            if ok:
                passed += 1

        except Exception as e:
            print(f"⚠️ {filename}: błąd ({e})")

    print(f"\nPodsumowanie: {passed}/{total} testów poprawnych ✅")