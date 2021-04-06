
class client_submission_data:

    @staticmethod
    def certify_features(features):
        return True

    def __init__(self, request):
        self.is_secceded = False
        try:
            if request.method == 'POST':
                print("checked post")
                if not True: # client_submission_data.certify_features(request.POST['features']):
                    print("checked features")
                    print("Error: failed to process features")
                else:
                    print('request is:' ,request.POST)
                    self.url = request.POST['url']
                    self.is_phishing = request.POST['is_phishing']
                    self.features = request.POST['features']
                    print("gdg")
                    self.is_secceded = True
            else:
                print("Error: wrong request method")
        except Exception as e:
            print("## Exception in data intiation:", e)
            self.is_secceded = False



        


