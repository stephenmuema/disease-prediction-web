# Create your views here.
import os

from rest_framework import generics

from api.models import Files
from api.serializers import FileSerializer
from djangoHealthAnalytics.settings import BASE_DIR


class FileList(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Files.objects.all()
    serializer_class = FileSerializer
# http http://127.0.0.1:8000/api/v1/files/ 'Authorization: Token 6c7494f9eb960d9027c12b282e57f06e7b974cc7'
def mergeCSVs():
        import pandas as pd

        import glob

        path = os.path.join(BASE_DIR, 'media', 'csv')  # use your path

        all_files = glob.glob(path + "/*.csv")

        li = []

        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)

            li.append(df)

        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.rename(columns={'dateprescribed': 'date', 'diagnosis': 'disease'})
        frame.drop('prescription', inplace=True, axis=1)
        # df.to_csv('my_csv.csv', mode='a', header=False)
        frame.to_csv('{}/data/Diseases1.csv'.format(self.BASE_DIR), mode='a', header=False)
