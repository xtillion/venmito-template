import os

def load_to_csv(data, filename, output_dir='output'):
    """
    Stores the specified pandas DataFrame in a CSV file within the given directory.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save DataFrame as CSV
    output_file = os.path.join(output_dir, filename)
    data.to_csv(output_file, index=False)
