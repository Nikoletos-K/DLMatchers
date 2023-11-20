import py_entitymatching as em
import io
import contextlib


A = em.read_csv_metadata('app/source.csv',sep='|',key='id')
B = em.read_csv_metadata('app/target.csv',sep='|',key='id')
print(A.columns)
print(B.columns)

print(set(['http://www.okkam.org/ontology_restaurant1.owl#street']).issubset(
             A.columns))
ob = em.OverlapBlocker()
C = ob.block_tables(A,
                    B,
                    'http://www.okkam.org/ontology_restaurant1.owl#street',
                    'http://www.okkam.org/ontology_restaurant2.owl#street',
                    word_level=True,
                    overlap_size=1, 
                    l_output_attrs=['http://www.okkam.org/ontology_restaurant1.owl#street', 'http://www.okkam.org/ontology_restaurant1.owl#name'], 
                    r_output_attrs=['http://www.okkam.org/ontology_restaurant2.owl#street', 'http://www.okkam.org/ontology_restaurant2.owl#name'],
                    show_progress=False)

ab = em.AttrEquivalenceBlocker()
D = ab.block_candset(C,
                     'http://www.okkam.org/ontology_restaurant1.owl#phone_number',
                     'http://www.okkam.org/ontology_restaurant2.owl#phone_number',
                     show_progress=False)



# feature_table = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)
# rb = em.RuleBasedBlocker()
# rb.add_rule(['http://www.okkam.org/ontology_restaurant1.owl#street_http://www.okkam.org/ontology_restaurant2.owl#street_lev(ltuple, rtuple) < 0.4'], feature_table)
# E = rb.block_tables(A,
#                     B,
#                     l_output_attrs=['http://www.okkam.org/ontology_restaurant1.owl#name'],
#                     r_output_attrs=['http://www.okkam.org/ontology_restaurant2.owl#name'],
#                     show_progress=False)

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    print(D)
blocking_output = buffer.getvalue()

with open('app/output.txt', 'w') as file:
    file.write(blocking_output)