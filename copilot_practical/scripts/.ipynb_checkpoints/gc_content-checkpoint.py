"""Print the GC content of each non-empty sequence in a FASTA file."""

import argparse
import warnings


def read_fasta_records(path):
    """Yield (header, sequence) pairs from a FASTA file."""
    header = None
    sequence = []

    with open(path, encoding="utf-8") as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line[1:]
                sequence = []
            elif header is not None:
                sequence.append("".join(line.split()))

    if header is not None:
        yield header, "".join(sequence)


def main():
    parser = argparse.ArgumentParser(
        description="Print GC content for each sequence in a FASTA file."
    )
    parser.add_argument("path", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="only print sequences with GC content above this percentage",
    )
    args = parser.parse_args()

    for header, sequence in read_fasta_records(args.path):
        if not sequence:
            warnings.warn(f"Skipping empty sequence for >{header}")
            continue

        sequence = sequence.upper()
        gc_count = sequence.count("G") + sequence.count("C")
        gc_percentage = gc_count / len(sequence) * 100
        if args.min_gc is not None and gc_percentage <= args.min_gc:
            continue
        print(f">{header}\t{gc_percentage:.2f}%")


if __name__ == "__main__":
    main()
