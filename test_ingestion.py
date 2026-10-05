from candidates.utils import process_candidate_file


result = process_candidate_file(
    'datasets/sample_candidates.csv',
    'datasets/output'
)

print("Accepted:")
print(result['accepted'])

print("\nRejected:")
print(result['rejected'])

print("\nAccepted file:")
print(result['accepted_file'])

print("\nRejected file:")
print(result['rejected_file'])