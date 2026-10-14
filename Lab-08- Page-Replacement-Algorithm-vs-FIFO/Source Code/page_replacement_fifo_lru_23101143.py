# Page Replacement Algorithms: FIFO vs LRU
# CSE 402: Operating System Lab | Lab Task 8

def fifo(pages, frames):
    mem = [None] * frames      # frame slots
    ptr = 0                    # slot holding the oldest page
    faults = 0
    trace = []
    for p in pages:
        if p in mem:
            status = "H"
        else:
            status = "F"
            faults += 1
            mem[ptr] = p                   # replace the oldest page
            ptr = (ptr + 1) % frames
        trace.append((p, mem[:], status))
    return faults, trace


def lru(pages, frames):
    mem = [None] * frames
    last_used = {}             # page -> time of most recent use
    faults = 0
    trace = []
    for t, p in enumerate(pages):
        if p in mem:
            status = "H"
        else:
            status = "F"
            faults += 1
            if None in mem:                # free frame available
                mem[mem.index(None)] = p
            else:                          # replace least recently used page
                victim = min(mem, key=lambda x: last_used[x])
                mem[mem.index(victim)] = p
        last_used[p] = t
        trace.append((p, mem[:], status))
    return faults, trace


def show(name, pages, frames, faults, trace):
    hits = len(pages) - faults
    print(f"\n{name} (frames = {frames})")
    print("Ref   : " + " ".join(f"{p:>2}" for p in pages))
    for f in range(frames):
        row = [("-" if t[1][f] is None else t[1][f]) for t in trace]
        print(f"Frame{f + 1}: " + " ".join(f"{x:>2}" for x in row))
    print("Result: " + " ".join(f"{t[2]:>2}" for t in trace))
    print(f"Page Faults = {faults} | Hits = {hits} | Hit Ratio = {hits / len(pages) * 100:.1f}%")


# ---------- Test 1: textbook reference string, 3 frames ----------
pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
frames = 3

fifo_faults, fifo_trace = fifo(pages, frames)
lru_faults, lru_trace = lru(pages, frames)

show("FIFO", pages, frames, fifo_faults, fifo_trace)
show("LRU", pages, frames, lru_faults, lru_trace)

n = len(pages)
print("\n--- Comparison (Test 1) ---")
print(f"{'Metric':<18}{'FIFO':<10}{'LRU':<10}")
print(f"{'Page Faults':<18}{fifo_faults:<10}{lru_faults:<10}")
print(f"{'Page Hits':<18}{n - fifo_faults:<10}{n - lru_faults:<10}")
print(f"{'Hit Ratio (%)':<18}{(n - fifo_faults) / n * 100:<10.1f}{(n - lru_faults) / n * 100:<10.1f}")

# ---------- Test 2: Belady's anomaly string, 3 vs 4 frames ----------
belady = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
print("\n--- Belady's Anomaly Test ---")
print(f"Reference string: {belady}")
print(f"{'Frames':<10}{'FIFO':<10}{'LRU':<10}")
for fr in (3, 4):
    f, _ = fifo(belady, fr)
    l, _ = lru(belady, fr)
    print(f"{fr:<10}{f:<10}{l:<10}")

# ---------- Verdict ----------
print("\n--- Result ---")
if lru_faults < fifo_faults:
    print(f"LRU is better: {lru_faults} faults vs {fifo_faults} for FIFO (Test 1).")
elif fifo_faults < lru_faults:
    print(f"FIFO is better: {fifo_faults} faults vs {lru_faults} for LRU (Test 1).")
else:
    print("Both algorithms perform equally (Test 1).")
