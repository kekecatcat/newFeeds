import news_recommendation_service_client as recommendation 

def test_basic():
    preference = recommendation.getPreferenceForUser('test_user')
    print (preference)
    assert len(preference) != 0
    print ("test_basic passed.")

if __name__ == "__main__":
    test_basic()