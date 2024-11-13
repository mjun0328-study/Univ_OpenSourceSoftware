import numpy as np
from sklearn import (datasets, ensemble, model_selection)
from sklearn.model_selection import GridSearchCV

if __name__ == '__main__':
    # Load a dataset
    wdbc = datasets.load_breast_cancer()

    # Define the model
    model = ensemble.GradientBoostingClassifier(random_state=42)

    # Define the parameter grid
    param_grid = {
        'n_estimators': [50, 100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7, 9],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'subsample': [0.8, 0.9, 1.0],
        'max_features': ['sqrt', 'log2', None]
    }

    # Perform GridSearchCV
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, return_train_score=True)
    grid_search.fit(wdbc.data, wdbc.target)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Evaluate the best model
    cv_results = model_selection.cross_validate(best_model, wdbc.data, wdbc.target, cv=5, return_train_score=True)
    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')