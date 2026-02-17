"""
Test script to demonstrate the filter_rates_by_target function
"""

def filter_rates_by_target(rates_list, target_amount):
    """
    Filter rates to show rows around the closest match to target_amount.

    Process:
    1. Find the row where credit_cost is closest to target_amount (by absolute difference)
    2. Sort all rows by interest_rate ascending
    3. Select: 2 rows with lower rate + closest match + 3 rows with higher rate
    4. Return as many as available if fewer exist
    """
    if not rates_list:
        return []

    # Filter out rates without valid credit_cost or interest_rate
    valid_rates = [
        r for r in rates_list
        if r.get('credit_cost') is not None and r.get('interest_rate') is not None
    ]

    if not valid_rates:
        return rates_list  # Return original if no valid rates

    # Step 1: Find the closest match to target_amount by absolute difference
    closest_match = min(
        valid_rates,
        key=lambda x: abs(x['credit_cost'] - target_amount)
    )

    # Step 2: Sort all rates by interest_rate ascending
    sorted_rates = sorted(valid_rates, key=lambda x: x['interest_rate'])

    # Step 3: Find the index of closest match in sorted list
    closest_index = sorted_rates.index(closest_match)

    # Step 4: Select surrounding rows
    # 2 rows before (lower rate) + closest match + 3 rows after (higher rate)
    start_index = max(0, closest_index - 2)
    end_index = min(len(sorted_rates), closest_index + 4)  # +1 for closest, +3 for higher

    selected_rates = sorted_rates[start_index:end_index]

    # Mark the closest match for reference
    for rate in selected_rates:
        rate['is_closest_to_target'] = (rate is closest_match)

    return selected_rates


# Test with sample data
if __name__ == "__main__":
    # Sample rate data
    sample_rates = [
        {"interest_rate": 6.5, "credit_cost": -3000, "monthly_payment": 1500},
        {"interest_rate": 6.0, "credit_cost": -1500, "monthly_payment": 1450},
        {"interest_rate": 7.0, "credit_cost": -4500, "monthly_payment": 1550},
        {"interest_rate": 5.5, "credit_cost": -500, "monthly_payment": 1400},
        {"interest_rate": 7.5, "credit_cost": -6000, "monthly_payment": 1600},
        {"interest_rate": 6.25, "credit_cost": -2200, "monthly_payment": 1475},
        {"interest_rate": 5.75, "credit_cost": -1000, "monthly_payment": 1425},
        {"interest_rate": 6.75, "credit_cost": -3500, "monthly_payment": 1525},
    ]

    target_amount = -2000

    print(f"\n{'='*80}")
    print(f"ORIGINAL DATA (unsorted):")
    print(f"{'='*80}")
    for i, rate in enumerate(sample_rates):
        print(f"{i+1}. Rate: {rate['interest_rate']}% | Credit/Cost: ${rate['credit_cost']:,} | Payment: ${rate['monthly_payment']}")

    print(f"\n{'='*80}")
    print(f"TARGET AMOUNT: ${target_amount:,}")
    print(f"{'='*80}")

    # Apply the filter
    filtered_rates = filter_rates_by_target(sample_rates, target_amount)

    print(f"\n{'='*80}")
    print(f"FILTERED RESULTS (sorted by rate, showing 2 lower + closest + 3 higher):")
    print(f"{'='*80}")
    for i, rate in enumerate(filtered_rates):
        closest_marker = " ← CLOSEST TO TARGET" if rate.get('is_closest_to_target') else ""
        diff = abs(rate['credit_cost'] - target_amount)
        print(f"{i+1}. Rate: {rate['interest_rate']}% | Credit/Cost: ${rate['credit_cost']:,} (diff: ${diff:,}){closest_marker}")

    print(f"\n{'='*80}")
    print(f"SUMMARY:")
    print(f"{'='*80}")
    print(f"Total original rates: {len(sample_rates)}")
    print(f"Filtered to: {len(filtered_rates)} rates")
    print(f"Closest match credit/cost: ${[r['credit_cost'] for r in filtered_rates if r.get('is_closest_to_target')][0]:,}")
    print(f"Rate range: {filtered_rates[0]['interest_rate']}% - {filtered_rates[-1]['interest_rate']}%")
    print(f"{'='*80}\n")

