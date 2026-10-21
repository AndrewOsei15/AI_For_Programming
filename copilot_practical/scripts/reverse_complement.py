# reverse_complement.py
# Reads a single-line DNA sequence from a FASTA file and prints its
# reverse complement.

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C", "N": "N"}

def read_fasta_sequence(path):
    """Return the sequence (str) from a single-record FASTA file."""
    sequence = []
    found_header = False
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if found_header:
                    raise ValueError("Expected a single-record FASTA file")
                found_header = True
                continue
            sequence.append("".join(line.split()))
    return "".join(sequence)

def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    seq = seq.upper()
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq))
    except KeyError as error:
        raise ValueError(
            f"Invalid DNA base: {error.args[0]!r}; expected A, T, C, G, or N"
        ) from error

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Print the reverse complement of a FASTA sequence.")
    parser.add_argument("path", help="path to a single-record FASTA file")
    args = parser.parse_args()
    seq = read_fasta_sequence(args.path)
    print(reverse_complement(seq))
