import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100000
TOLERANCE = 0.001


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
    probability = {corp: (1 - damping_factor) / len(corpus) for corp in corpus}
    
    prob_link = damping_factor / len(corpus[page]) if len(corpus[page]) != 0 else 0
    for link in corpus[page]:
        probability[link] += prob_link

    total = sum(probability.values())
    for corp in probability:
        probability[corp] /= total

    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {page: 0 for page in corpus}
    pages = list(corpus.keys())
    page = random.choice(pages)

    for _ in range(n):
        pagerank[page] += 1
        probability = transition_model(corpus, page, damping_factor)
        page = random.choices(pages, weights=probability.values(), k=1)[0]
    
    for p in pagerank:
        pagerank[p] /= n

    return pagerank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}
    new_pagerank = {page: 0 for page in corpus}
    delta = float('inf')
     
    while delta > TOLERANCE:   
        # calculate the pagerank for each page
        for page in corpus:
            pr = (1 - damping_factor) / N

            for other_page in corpus:
                if page in corpus[other_page]:
                    pr += damping_factor * pagerank[other_page] / len(corpus[other_page])
                elif len(corpus[other_page]) == 0:
                    pr += damping_factor * pagerank[other_page] / N

            new_pagerank[page] = pr

        # get the difference between the old and new pageranks for each page
        delta = max([abs(new_pagerank[page] - pagerank[page]) for page in pagerank])
        pagerank = new_pagerank.copy()

    return pagerank


if __name__ == "__main__":
    main()
