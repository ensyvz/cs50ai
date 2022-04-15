import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dist = dict()
    link_count = len(corpus[page])

    if link_count == 0:
        for p in corpus.keys():
            prob_dist[p] = 1 / len(corpus)
    else:
        for p in corpus.keys():
            if p not in corpus[page]:
                prob_dist[p] = (1-damping_factor) / len(corpus)
            else:
                prob = damping_factor * (1/link_count)
                prob += (1-damping_factor) / len(corpus)
                prob_dist[p] = prob
        prob_dist[page] = (1-damping_factor) / len(corpus)

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict()
    pages = list(corpus.keys())

    def order_dist(dist_dict):
        ordered_list = list(dist_dict)
        for i in range(len(pages)):
            ordered_list[i] = dist_dict[pages[i]]
        return ordered_list
    
    for page in corpus.keys():
        page_ranks[page] = 0

    current_page = random.choice(pages)
    page_ranks[current_page] += 1
    for i in range(n-1):
        prob_dist = transition_model(corpus,current_page,damping_factor)
        ordered_dist = order_dist(prob_dist)
        current_page = random.choices(pages,weights = ordered_dist)[0]
        page_ranks[current_page] += 1
    for page in page_ranks:
        page_ranks[page] /= n

    return page_ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict()
    for page in corpus.keys():
        page_ranks[page] = 1/len(corpus)
    
    flag = 0
    while flag != len(corpus):
        flag = 0
        new_ranks = page_ranks.copy()
        for page in corpus:
            new_pr = (1-damping_factor)/len(corpus)
            total = 0
            for i in corpus:
                if len(corpus[i])==0:
                    total += page_ranks[i]/len(corpus)
                elif page in corpus[i]:
                    total += page_ranks[i]/len(corpus[i])
            new_pr += damping_factor*total
            if abs(page_ranks[page]-new_pr) < 0.001:
                flag += 1
            new_ranks[page] = new_pr
        if flag != len(corpus):
            page_ranks = new_ranks
    
    return page_ranks

if __name__ == "__main__":
    main()
