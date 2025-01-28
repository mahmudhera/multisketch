import argparse
import random
import mmh3
from tqdm import tqdm
import matplotlib.pyplot as plt


def create_classic_sketch(set_, seed, scale_factor):
    threshold = 1.0 * 2**32 * scale_factor
    sketch = set()
    for item in set_:
        # compute the hash value of the item
        hash_value = mmh3.hash(str(item), seed, False)
        if hash_value <= threshold:
            sketch.add(hash_value)
    return sketch
        


def create_set(size):
    return set(random.randint(0, 2**31) for _ in range(size))


def compute_containment(set1, set2):
    intersection_size = len(set1 & set2)
    return intersection_size / len(set1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size1', type=int, default=10000)
    parser.add_argument('--size2', type=int, default=10000)
    parser.add_argument('--num_common', type=int, default=1000)
    parser.add_argument('--n_iter', type=int, default=100)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--scale_factor', type=float, default=0.01)
    parser.add_argument('--num_multisketches', type=int, default=2)
    return parser.parse_args()


def main():
    args = parse_args()
    random.seed(args.seed)
    
    # create first set
    set1 = create_set(args.size1)
    
    # create second set by adding common elements
    common_elements = random.sample(list(set1), args.num_common)
    set2 = create_set(args.size2)
    set2.update(common_elements)
    
    containment_true = compute_containment(set1, set2)
    print(f"True containment: {containment_true}")
    
    bias_factor = 1 - (1 - args.scale_factor)**args.size1
    print(f"Bias factor: {bias_factor}")
    
    # create a list of seeds for fracminhash sketches
    seeds = random.sample(range(2**32), args.n_iter)
    
    # for every seed, compute sketches of the sets, and then compute the containment
    containments_classic = []
    for seed in tqdm(seeds):
        sketch1 = create_classic_sketch(set1, seed, args.scale_factor)
        sketch2 = create_classic_sketch(set2, seed, args.scale_factor)
        
        containment = compute_containment(sketch1, sketch2)
        containments_classic.append(containment)
        
    # compute the average containment, and the standard deviation
    avg_containment = sum(containments_classic) / len(containments_classic)
    std_containment = (sum((c - containment_true)**2 for c in containments_classic) / len(containments_classic))**0.5
    
    print(f"Average containment (classic): {avg_containment}")
    print(f"Standard deviation from true (classic): {std_containment}")
    
    
    containments_multisketch = []
    for seed in tqdm(seeds):
        separate_containments = []
        for i in range(args.num_multisketches):
            # create a random seed 
            seed = random.randint(0, 2**32)
            scale_factor_to_use = args.scale_factor / args.num_multisketches
            sketch1 = create_classic_sketch(set1, seed, scale_factor_to_use)
            sketch2 = create_classic_sketch(set2, seed, scale_factor_to_use)
            containment = compute_containment(sketch1, sketch2)
            separate_containments.append(containment)
        avg_containment = sum(separate_containments) / len(separate_containments)
        containments_multisketch.append(avg_containment)
        
    avg_containment = sum(containments_multisketch) / len(containments_multisketch)
    std_containment = (sum((c - containment_true)**2 for c in containments_multisketch) / len(containments_multisketch))**0.5
    
    print(f"Average containment (multisketch): {avg_containment}")
    print(f"Standard deviation from true (multisketch): {std_containment}")
    
    # plot the distrbutions of the two containments
    plt.hist(containments_classic, bins=20, alpha=0.5, label='classic')
    plt.hist(containments_multisketch, bins=20, alpha=0.5, label='multisketch')
    plt.legend()
    plt.show()
    
    
if __name__ == "__main__":
    main()
    