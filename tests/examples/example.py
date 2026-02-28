def bedder_n_overlapping(fragment) -> int:
    return len(fragment.b)

def bedder_total_b_overlap(fragment) -> int:
    return sum(b.stop - b.start for b in fragment.b)

