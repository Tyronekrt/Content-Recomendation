from celery import shared_task
from myapp.models import Content, UserHistory
from surprise import SVD, Dataset, Reader
import pickle
import pandas as pd
from celery import Celery
from celery.schedules import crontab

app = Celery('ContentRecommendation')
app.conf.beat_schedule = {
    'retrain-model-every-week': {
        'task': 'myapp.tasks.retrain_model',
        'schedule': crontab(minute=0, hour=0, day_of_week=0),  # every Sunday at midnight
    },
}

@shared_task
def retrain_model():
    # Load user history and retrain the model
    data = pd.read_csv('ContentRecommendation/ml-1m/ratings.dat')
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(data[['user_id', 'item_id', 'rating']], reader)
    trainset = dataset.build_full_trainset()

    model = SVD()
    model.fit(trainset)

    # Save the model to a file
    with open('collaborative_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    print("Model retrained and saved.")
