import py_entitymatching as em
import io
import contextlib


A = em.read_csv_metadata('app/source.csv',sep='|',key='id')
B = em.read_csv_metadata('app/target.csv',sep='|',key='id')
S = em.read_csv_metadata('app/labeled.csv', 
                         sep='|',key='id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_id', fk_rtable='rtable_id')

IJ = em.split_train_test(S, train_proportion=0.5, random_state=0)
I = IJ['train']
J = IJ['test']


dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')

F = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)

H = em.extract_feature_vecs(I, 
                            feature_table=F, 
                            attrs_after='label',
                            show_progress=False)

H = em.impute_table(H, 
                exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'label'],
                strategy='mean')

result = em.select_matcher([dt, rf, svm, ln, lg], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'label'],
        k=5,
        target_attr='label', metric_to_select_matcher='f1', random_state=0)


buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    print(result['cv_stats'])
output = buffer.getvalue()

with open('app/output.txt', 'w') as file:
    file.write(output)

# ob = em.OverlapBlocker()
# C = ob.block_tables(A,
#                     B,
#                     'http://www.okkam.org/ontology_restaurant1.owl#street',
#                     'http://www.okkam.org/ontology_restaurant2.owl#street',
#                     word_level=True,
#                     overlap_size=1, 
#                     l_output_attrs=['http://www.okkam.org/ontology_restaurant1.owl#street', 'http://www.okkam.org/ontology_restaurant1.owl#name'], 
#                     r_output_attrs=['http://www.okkam.org/ontology_restaurant2.owl#street', 'http://www.okkam.org/ontology_restaurant2.owl#name'],
#                     show_progress=False)

# ab = em.AttrEquivalenceBlocker()
# D = ab.block_candset(C,
#                      'http://www.okkam.org/ontology_restaurant1.owl#phone_number',
#                      'http://www.okkam.org/ontology_restaurant2.owl#phone_number',
#                      show_progress=False)



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