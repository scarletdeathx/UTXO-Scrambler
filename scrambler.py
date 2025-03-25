import configparser
import json
from decimal import Decimal, ROUND_DOWN
import secrets
from datetime import datetime

def random_split(total, parts, min_amt, max_amt, tries=10000):
    """Distributes `total` among `parts` securely and randomly, keeping each part within [min_amt, max_amt]."""
    rng = secrets.SystemRandom()
    for _ in range(tries):
        factors = [Decimal(rng.random()) for _ in range(parts)]
        factor_sum = sum(factors)
        split = [(f / factor_sum * total).quantize(Decimal("0.00000001"), rounding=ROUND_DOWN) for f in factors]
        diff = total - sum(split)
        split[0] = (split[0] + diff).quantize(Decimal("0.00000001"), rounding=ROUND_DOWN)
        if all(min_amt <= amt <= max_amt for amt in split):
            return split
    raise ValueError("Failed to generate valid random split after multiple attempts.")

def load_addresses(filename):
    """Loads output addresses from a file."""
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def log_transaction(log_file, data):
    """Logs data to the specified log file."""
    try:
        with open(log_file, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {json.dumps(data, indent=2)}\n")
        print(f"Transaction successfully logged to {log_file}")
    except Exception as e:
        print(f"Error logging transaction: {e}")

def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read("scrambler.conf")

    fee = Decimal(config.get("DEFAULT", "fee", fallback="0.001"))
    outputs_file = config.get("DEFAULT", "outputs_file", fallback="outputs.txt")
    change_address = config.get("DEFAULT", "change_address", fallback="CHANGE_ADDRESS")
    min_output = Decimal(config.get("DEFAULT", "min_output", fallback="0.01"))
    max_output = Decimal(config.get("DEFAULT", "max_output", fallback="9.99999999"))
    log_enabled = config.getboolean("DEFAULT", "log_enabled", fallback=False)
    log_file = config.get("DEFAULT", "log_file", fallback="scrambler.log")
    change_percent = Decimal(config.get("DEFAULT", "change_percent", fallback="0"))

    # Load output addresses from file
    addresses = load_addresses(outputs_file)
    if not addresses:
        print("No output addresses found in the file!")
        return

    # Load UTXO inputs from file
    try:
        with open("inputs.json", "r") as f:
            utxos = json.load(f)
        if not isinstance(utxos, list):
            raise ValueError("Expected a list of UTXO objects, but got something else.")
    except Exception as e:
        print(f"Error reading or parsing inputs.json: {e}")
        return

    # Calculate total funds available
    total_amount = sum(Decimal(str(utxo["amount"])) for utxo in utxos)
    if total_amount <= fee:
        print("Insufficient funds to cover the fee!")
        return

    distributable = total_amount - fee

    # Calculate change and random allocation
    change_amount = (distributable * change_percent / 100).quantize(Decimal("0.00000001"), rounding=ROUND_DOWN)
    random_amount = distributable - change_amount

    if random_amount < len(addresses) * min_output:
        print(f"Insufficient funds to meet minimum output of {min_output} GRC per address!")
        return

    max_distributable = len(addresses) * max_output
    target_total = min(random_amount, max_distributable)

    # Randomly distribute the funds among output addresses
    try:
        amounts = random_split(target_total, len(addresses), min_output, max_output)
    except Exception as e:
        print(f"Error distributing funds: {e}")
        return

    outputs = {addr: float(amt) for addr, amt in zip(addresses, amounts)}

    # Add leftover change to the change address
    if change_amount > 0:
        outputs[change_address] = float(change_amount)

    # Create raw transaction
    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]} for utxo in utxos]

    raw_tx = {
        "inputs": inputs,
        "outputs": outputs
    }

    # Optionally log the raw transaction
    if log_enabled:
        log_transaction(log_file, raw_tx)

    # Print the raw transaction and CLI command
    print("\n=== RAW TRANSACTION ===")
    print(json.dumps(raw_tx, indent=2))
    print("\nTo broadcast your transaction, use the following CLI command:")
    print(f"gridcoin-cli createrawtransaction '{json.dumps(inputs)}' '{json.dumps(outputs)}'")

if __name__ == "__main__":
    main()
