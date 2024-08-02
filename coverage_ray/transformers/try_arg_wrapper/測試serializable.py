import pickle


def check_serializable(obj):
    try:
        pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        return True
    except Exception as e:
        return False


def test_func(a):
    print(a)


print(check_serializable(pickle))
