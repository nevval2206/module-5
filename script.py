import random

# --- Parameters ---
num_packets = 10000   # Gönderilen toplam paket sayısı
p_success = 0.95      # Tek bir gönderimin başarı olasılıgi
strategies = ["single_send", "double_send", "retry_if_lost"]

# --- Results Dictionary ---
results = {}

for strategy in strategies:
    successes = 0
    total_cost = 0

    for _ in range(num_packets):
        if strategy == "single_send":
            # Paket bir kez gönderilir
            total_cost += 1
            if random.random() < p_success:
                successes += 1

        elif strategy == "double_send":
            # Aynı paket iki kez gönderilir
            total_cost += 2
            # Eğer herhangi biri başarılıysa paket ulaşır
            if random.random() < p_success or random.random() < p_success:
                successes += 1

        elif strategy == "retry_if_lost":
            # Önce bir kez gönder
            total_cost += 1
            if random.random() < p_success:
                successes += 1
            else:
                # Kaybolursa tekrar gönder (1 kez)
                total_cost += 1
                if random.random() < p_success:
                    successes += 1

    reliability = successes / num_packets
    efficiency = successes / total_cost

    results[strategy] = {
        "reliability": reliability,
        "efficiency": efficiency,
        "total_cost": total_cost
    }

# --- Print Results ---
print("=== Reliability and Efficiency Comparison ===")
for strategy, metrics in results.items():
    print(f"\nStrategy: {strategy}")
    print(f"Reliability (Success Rate): {metrics['reliability']:.4f}")
    print(f"Efficiency (Success per Cost): {metrics['efficiency']:.4f}")
    print(f"Total Cost Used: {metrics['total_cost']}")
