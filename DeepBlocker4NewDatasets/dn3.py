import time
import pandas as pd
from deep_blocker import DeepBlocker
from tuple_embedding_models import  AutoEncoderTupleEmbedding, CTTTupleEmbedding, HybridTupleEmbedding
from vector_pairing_models import ExactTopKVectorPairing
import blocking_utils

deli = '%'
main_dir = "/home/gpapadakis/data/fastText/dbdata/"
left_df = pd.read_csv(main_dir + "D4Bemb.csv", sep=deli)
left_df = left_df[['id', 'Clean Ag.Value']]
right_df = pd.read_csv(main_dir + "D4Aemb.csv", sep=deli)
right_df = right_df[['id', 'Clean Ag.Value']]
golden_df = pd.read_csv(main_dir + "D4groundtruthRev.csv", sep=deli)
cols_to_block = ["Clean Ag.Value"]

k = 1
        
tuple_embedding_model = AutoEncoderTupleEmbedding()
topK_vector_pairing_model = ExactTopKVectorPairing(K=k)
db = DeepBlocker(tuple_embedding_model, topK_vector_pairing_model)
candidate_set_df = db.block_datasets(left_df, right_df, cols_to_block)
    
results = blocking_utils.compute_blocking_statistics(candidate_set_df, golden_df, left_df, right_df)
candidate_set_df.to_csv(main_dir + "D4candidates.csv", sep=deli, index=False)
print(results)
