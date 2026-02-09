import pandas as pd
from app.fairness import run_fairness_audit
from app.scoring import calculate_fairness_score, interpret_bias
from app.mitigation import recommend_mitigation

if __name__ == '__main__':
    path = r"..\sample_data\tabular_hiring_bias.csv"
    df = pd.read_csv(path)
    # ensure columns exist
    print('Columns:', df.columns.tolist())
    report = run_fairness_audit(df, sensitive='gender', y_true='label', y_pred='prediction')
    score = calculate_fairness_score(report['metrics'])
    mitigation = recommend_mitigation(report['metrics'])
    print('\nReport metrics:')
    print(report['metrics'])
    print('\nFairness score:', score)
    print('Bias level:', interpret_bias(score))
    print('\nMitigation:')
    for m in mitigation:
        print('-', m)
