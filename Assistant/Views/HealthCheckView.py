from AiVoice.BaseClasses.CrofarmView import CrofarmView


class HealthCheckView(CrofarmView):

    def get(self, request, version_id):
        return self.getResWithData({"data":"Health check is ok"})
