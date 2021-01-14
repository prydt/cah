from sentence_transformers import SentenceTransformer

from reader import CAH

file = "data/json-against-humanity/compact.md.json"

model = SentenceTransformer("roberta-base-nli-stsb-mean-tokens")
game = CAH(file)

black_cards = [str(b) for deck in game.values() for b in deck.black_cards]
white_cards = [str(w) for deck in game.values() for w in deck.white_cards]

cards = black_cards + white_cards
print(cards)
sentence_embeddings = model.encode(cards)

from sklearn.cluster import KMeans

num_clusters = 5
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(sentence_embeddings)
cluster_assigment = clustering_model.labels_

clustered_sents = [[]] * num_clusters
for s_id, c_id in enumerate(cluster_assigment):
    clustered_sents[c_id].append(cards[s_id])

for i, cluster in enumerate(clustered_sents):
    print("Cluster ", i + 1)
    print(cluster)
    print()
