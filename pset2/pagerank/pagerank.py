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

    print(f"\nPageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)

    print(f"\nPageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print("\n")


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
    model = dict()

    # probability of randomly choosing one of the links from page
    if (len(corpus[page])):
        linkProb = damping_factor/len(corpus[page])

    # probability of randomly choosing one of all pages in the corpus with equal probability.
    if (len(corpus)):
        randProb = (1 - damping_factor)/len(corpus)

    # if page has outgoing links
    if corpus[page]:

        # assign probability distribution of pages linked
        for link in corpus:
            if link in corpus[page]:
                model[link] = linkProb + randProb
            else:
                model[link] = randProb
    else:

        # assign a probability distribution that chooses randomly among all pages with equal probability
        for link in corpus:
            model[link] = 1/len(corpus)

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    model = dict()

    # set initial probabilty of each page to zero
    for page in corpus:
        model[page] = 0

    sum = 0
    # choose a page randomly and get its transition model
    page = random.choices(list(corpus.keys()))[0]
    model[page] += 1/n
    sum += 1/n
    trans = transition_model(corpus, page, damping_factor)

    # sample `n-1` pages according to transition models
    for i in range(n-1):
        page = random.choices(list(trans.keys()), weights=trans.values())[0]
        model[page] += 1/n
        sum += 1/n
        trans = transition_model(corpus, page, damping_factor)

    return model


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    model = dict()

    # set initial page ranks
    if (len(corpus) != 0):
        for page in corpus:
            model[page] = 1/len(corpus)

    while True:
        # get a copy of the model
        currentModel = model.copy()

        check = 0

        # assign a page rank for each page
        for page in corpus:
            sum = 0

            for link in corpus:
                if (corpus[link]):
                    if (page in corpus[link]):
                        numLinks = len(corpus[link])
                        sum += currentModel[link]/numLinks
                else:

                    numLinks = len(corpus)
                    sum += currentModel[link]/numLinks

            pr = ((1 - damping_factor)/len(corpus)) + (damping_factor * sum)

            # check if values of page rank converged
            if (abs(pr - model[page]) < 0.001):

                model[page] = pr
                check += 1
            else:

                model[page] = pr
                check = 0

        if check == len(corpus):
            break

    return model


if __name__ == "__main__":
    main()
