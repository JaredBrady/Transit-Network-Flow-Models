import subprocess

def run_glpk(model_file, data_file):
    result = subprocess.run(
        ["glpsol", "-m", model_file, "-d", data_file],
        capture_output=True,
        text=True
    )

    if result.stderr:
        print(result.stderr)

    for line in result.stdout.splitlines():
        if (
            "OPTIMAL" in line
            or "Total cost" in line
            or "Wrote solution" in line
            or "Model has been successfully processed" in line
        ):
            print(line)

    return result

def print_glpk_block(result, start_label, end_label=None):
    printing = False

    for line in result.stdout.splitlines():
        if start_label in line:
            printing = True

        if printing:
            print(line)

        if end_label is not None and end_label in line:
            break